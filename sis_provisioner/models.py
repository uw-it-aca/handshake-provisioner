# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import utc
from sis_provisioner.dao.file import read_file, write_file
from sis_provisioner.dao.handshake import write_file as write_handshake
from sis_provisioner.dao.student import get_students_for_handshake
from sis_provisioner.dao.term import AcademicTerm
from sis_provisioner.utils import (
    get_majors, get_major_names, get_primary_major_name, is_athlete,
    is_veteran, get_synced_college_name, get_ethnicity_name, get_class_desc,
    format_student_number, format_name)
from datetime import datetime
import csv
import io
import os


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


class ImportFileManager(models.Manager):
    def import_file(self):
        try:
            import_file = super().get_queryset().latest('created_date')
            import_file.sisimport()

        except ImportFile.DoesNotExist:
            pass


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_test_file = models.BooleanField(default=False)
    created_date = models.DateTimeField()
    processed_date = models.DateTimeField(null=True)
    processed_status = models.CharField(max_length=128, null=True)

    objects = ImportFileManager()

    @property
    def filename(self):
        return os.path.basename(self.path or '')

    @property
    def content(self):
        return read_file(self.path)

    def create_path(self):
        name = self.term.name
        prefix = getattr(settings, 'FILENAME_PREFIX')
        if self.is_test_file and prefix is not None and len(prefix):
            name = '{}-{}'.format(prefix, name)

        if self.created_date is None:
            self.created_date = datetime.utcnow().replace(tzinfo=utc)

        self.path = self.created_date.strftime(
            '%Y/%m/{}-%Y%m%d-%H%M%S.csv'.format(name))
        return self.path

    def sisimport(self):
        write_handshake(self.filename, self.content)
        self.processed_date = datetime.utcnow().replace(tzinfo=utc)
        self.processed_status = 200
        self.save()

    def create(self):
        write_file(self.create_path(), self._generate_csv())
        self.save()

    def json_data(self):
        return {
            'id': self.pk,
            'name': self.filename,
            'term': self.term.json_data(),
            'is_test_file': self.is_test_file,
            'download_url': reverse('import-file', kwargs={
                'file_id': self.pk}),
            'created_date': self.created_date.isoformat(),
            'processed_date': self.processed_date.isoformat() if (
                self.processed_date is not None) else None,
            'processed_status': self.processed_status,
        }

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
                get_class_desc(person.student.class_code, majors),
                last_name,
                first_name,
                middle_name,
                person.preferred_first_name,
                get_synced_college_name(majors),
                '{}@{}'.format(person.uwnetid, settings.EMAIL_DOMAIN),
                person.student.campus_desc,
                get_major_names(majors),
                get_primary_major_name(majors),
                'TRUE',
                # person.student.gender,
                # get_ethnicity_name(person.student.ethnicities),
                # is_athlete(person.student.special_program_code),
                # is_veteran(person.student.veteran_benefit_code),
                # 'work_study_eligible',  # TODO: get from visa type
                # 'primary_education:education_level_name',  # TODO: ?
            ])

        return s.getvalue()
