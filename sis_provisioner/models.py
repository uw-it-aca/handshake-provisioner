# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.timezone import utc
from sis_provisioner.exceptions import EmptyQueryException
from sis_provisioner.dao.file import read_file, write_file, delete_file
from sis_provisioner.dao.handshake import write_file as write_handshake
from sis_provisioner.dao.student import (
    get_students_for_handshake, get_active_students)
from sis_provisioner.dao.term import AcademicTerm
from sis_provisioner.utils import (
    get_majors, get_major_names, get_primary_major_name, is_athlete,
    is_veteran, get_college_name, get_ethnicity_name, get_class_desc,
    format_student_number, format_name)
from datetime import datetime
from logging import getLogger
import csv
import io
import os

logger = getLogger(__name__)


class TermManager(models.Manager):
    def current(self):
        academic_term = AcademicTerm()

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=academic_term.quarter)
        return term

    def next(self):
        academic_term = AcademicTerm().next()

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=academic_term.quarter)
        return term


class Term(models.Model):
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4

    QUARTER_CHOICES = (
        (WINTER, 'WIN'), (SPRING, 'SPR'), (SUMMER, 'SUM'), (AUTUMN, 'AUT')
    )

    year = models.SmallIntegerField()
    quarter = models.SmallIntegerField(choices=QUARTER_CHOICES)

    objects = TermManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'quarter'],
                                    name='unique_term')
        ]

    @property
    def name(self):
        return '{}{}'.format(
            dict(self.QUARTER_CHOICES).get(self.quarter), self.year)

    def json_data(self):
        return {
            'id': self.pk,
            'year': self.year,
            'quarter': dict(self.QUARTER_CHOICES).get(self.quarter),
        }

    def next(self):
        next_term = AcademicTerm(year=self.year, quarter=self.quarter).next()
        term, _ = Term.objects.get_or_create(
            year=next_term.year, quarter=next_term.quarter)
        return term


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    created_by = models.CharField(max_length=32, default='automatic')
    created_date = models.DateTimeField()
    generated_date = models.DateTimeField(null=True)
    import_progress = models.SmallIntegerField(default=0)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.CharField(max_length=128, null=True)
    process_id = models.CharField(max_length=64, null=True)

    class Meta:
        abstract = True

    @property
    def filename(self):
        return os.path.basename(self.path or '')

    @property
    def content(self):
        if self.generated_date is not None:
            return read_file(self.path)

    def build(self):
        self.process_id = os.getpid()
        self.save()
        try:
            write_file(self.path, self._generate_csv())
            self.generated_date = datetime.utcnow().replace(tzinfo=utc)
            logger.info('CSV generated for file ID {}'.format(self.pk))
        except EmptyQueryException as ex:
            logger.info('CSV skipped for file ID {}: No students'.format(
                self.pk, ex))
        except Exception as ex:
            logger.info('CSV failed for file ID {}: {}'.format(
                self.pk, ex))

        self.process_id = None
        self.save()

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = datetime.utcnow().replace(tzinfo=utc)
        if self.path is None:
            self.path = self._create_path()
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        if self.generated_date is not None:
            delete_file(self.path)
        super().delete(**kwargs)

    def json_data(self):
        return {
            'id': self.pk,
            'name': self.filename,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat() if (
                self.created_date is not None) else None,
            'generated_date': self.generated_date.isoformat() if (
                self.generated_date is not None) else None,
            'import_progress': self.import_progress,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'process_id': self.process_id,
        }

    def sisimport(self):
        raise NotImplemented()

    def _create_path(self):
        raise NotImplemented()

    def _generate_csv(self):
        raise NotImplemented()


class HandshakeStudentsFileManager(models.Manager):
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


class HandshakeStudentsFile(ImportFile):
    '''
    A file containing enrolled students for a term, used for provisioning
    student attributes to Handshake.
    '''
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_test_file = models.BooleanField(default=False)

    objects = HandshakeStudentsFileManager()

    def sisimport(self):
        if self.generated_date is None:
            raise ObjectDoesNotExist

        try:
            write_handshake(self.filename, self.content)
            self.imported_status = 200
            logger.info('File ID {} imported'.format(self.pk))
        except Exception as ex:
            logger.critical(ex, exc_info=True)
            self.imported_status = 500

        self.imported_date = datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def json_data(self):
        data = super().json_data()
        data['term'] = self.term.json_data()
        data['is_test_file'] = self.is_test_file
        data['api_path'] = reverse('handshake-file', kwargs={
                'file_id': self.pk}),
        return data

    def _create_path(self):
        name = self.term.name
        prefix = getattr(settings, 'FILENAME_TEST_PREFIX')

        if self.is_test_file and prefix is not None and len(prefix):
            name = '{}-{}'.format(prefix, name)

        return self.created_date.strftime(
            '%Y/%m/{}-%Y%m%d-%H%M%S.csv'.format(name))

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.HANDSHAKE_CSV_HEADER)

        for person in get_students_for_handshake(self.term):
            majors = get_majors(person.student)

            first_name, middle_name, last_name = format_name(person.first_name,
                                                             person.surname)

            writer.writerow([
                person.uwnetid,
                person.uwnetid,
                format_student_number(person.student.student_number),
                get_class_desc(person.student, majors),
                last_name,
                first_name,
                middle_name,
                person.preferred_first_name,
                get_college_name(majors, person.student.campus_code),
                '{}@{}'.format(person.uwnetid, settings.EMAIL_DOMAIN),
                person.student.campus_desc,
                get_major_names(majors),
                get_primary_major_name(majors),
                'TRUE',  # primary_education:currently_attending
                person.student.gender,
                get_ethnicity_name(person.student.ethnicities),
                'TRUE' if is_athlete(person.student) else 'FALSE',
                'TRUE' if is_veteran(person.student) else 'FALSE',
                # 'work_study_eligible',
                # 'primary_education:education_level_name',
            ])

        return s.getvalue()


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
        return self.created_date.strftime(
            '%Y/%m/active-students-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow([
            'email', 'uwregid', 'prior_uwnetids', 'prior_uwregids'])

        for person in get_active_students():
            writer.writerow([
                '{}@{}'.format(person.uwnetid, settings.EMAIL_DOMAIN),
                person.uwregid,
                ';'.join(person.prior_uwnetids),
                ';'.join(person.prior_uwregids),
            ])

        return s.getvalue()
