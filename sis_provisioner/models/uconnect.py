# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.timezone import get_default_timezone
from sis_provisioner.models.importfile import ImportFile
from sis_provisioner.models.term import Term
from sis_provisioner.dao.uconnect import write_file
from sis_provisioner.dao.student import get_students_for_uconnect
from datetime import datetime, timezone
from logging import getLogger
import csv
import io

logger = getLogger(__name__)


class UconnectStudentsFileManager(models.Manager):
    def build_file(self):
        import_file = super().get_queryset().filter(
            generated_date__isnull=True, process_id__isnull=True
        ).order_by('created_date').first()

        if import_file is None:
            return

        import_file.build()

        # Automatically created files are automatically imported
        if (import_file.generated_date is not None and
                import_file.created_by == 'automatic'):
            import_file.sisimport()

        return import_file


class UconnectStudentsFile(ImportFile):
    '''
    A file containing enrolled students for a term, used for provisioning
    student attributes to UConnect.
    '''
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_test_file = models.BooleanField(default=False)

    objects = UconnectStudentsFileManager()

    def sisimport(self):
        if self.generated_date is None:
            raise ObjectDoesNotExist

        try:
            write_file(settings.UCONNECT_FILENAME, self.content)
            self.imported_status = 200
            self.imported_date = datetime.now(timezone.utc)
            logger.info(f'File ID {self.pk} imported')
        except Exception as ex:
            logger.critical(ex, exc_info=True)
            self.imported_status = 500
            raise
        finally:
            self.save()

    def json_data(self):
        data = super().json_data()
        data['term'] = self.term.json_data()
        data['is_test_file'] = self.is_test_file
        data['type'] = 'uConnect'
        data['api_path'] = reverse('uconnect-file', kwargs={
            'file_id': self.pk})
        return data

    def _create_path(self):
        name = self.term.name
        prefix = getattr(settings, 'FILENAME_TEST_PREFIX')

        if self.is_test_file and prefix is not None and len(prefix):
            name = f'{prefix}-{name}'

        local_tz = get_default_timezone()
        return self.created_date.replace(tzinfo=timezone.utc).astimezone(
            local_tz).strftime(f'%Y/%m/{name}-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.UCONNECT_CSV_HEADER)

        for student in get_students_for_uconnect(self.term):
            writer.writerow([
                '',
                '',
                f'{student.person.uwnetid}@{settings.EMAIL_DOMAIN}',
                student.person.uwnetid,
                "",
                "",
                "",
            ])

        return s.getvalue()
