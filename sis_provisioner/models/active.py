# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from django.conf import settings
from django.utils.timezone import get_default_timezone
from sis_provisioner.models.importfile import ImportFile
from sis_provisioner.dao.student import get_active_students
from datetime import timezone
from logging import getLogger
import csv
import io

logger = getLogger(__name__)


class ActiveStudentsFileManager(models.Manager):
    def build_file(self):
        import_file = super().get_queryset().filter(
            generated_date__isnull=True, process_id__isnull=True
        ).order_by('created_date').first()

        if import_file is not None:
            import_file.build()
            return import_file


class ActiveStudentsFile(ImportFile):
    '''
    A file containing all active students, currently used for provisioning
    uwnetid and uwregid to LinkedIn Learning.
    '''
    objects = ActiveStudentsFileManager()

    def _create_path(self):
        local_tz = get_default_timezone()
        return self.created_date.replace(tzinfo=timezone.utc).astimezone(
            local_tz).strftime('%Y/%m/active-students-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow([
            'email', 'uwregid', 'prior_uwnetids', 'prior_uwregids'])

        for person in get_active_students():
            writer.writerow([
                f'{person.uwnetid}@{settings.EMAIL_DOMAIN}',
                person.uwregid,
                ';'.join(person.prior_uwnetids),
                ';'.join(person.prior_uwregids),
            ])

        return s.getvalue()
