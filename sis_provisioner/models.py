# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from django.utils.timezone import utc
from sis_provisioner.dao.file import read_file, write_file
from sis_provisioner.dao.student import get_students_for_handshake
from sis_provisioner.utils import (
    valid_major_codes, get_major_names, get_primary_major_name, is_athlete,
    is_veteran, get_synced_college_name, get_ethnicity_name, get_class_desc,
    format_student_number, format_name)
from dateutil.relativedelta import relativedelta
from datetime import datetime
import csv
import io


class AcademicTerm():
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4

    QTR_NAMES = {WINTER: 'WIN', SPRING: 'SPR', SUMMER: 'SUM', AUTUMN: 'AUT'}

    def __init__(self, date=None):
        if date is None:
            date = datetime.now()

        self._date = date
        self.current()

    def current(self):
        year, quarter = self._term_from_datetime(self._date)
        self.year = year
        self.quarter = quarter
        return self

    def next(self):
        if self.quarter == self.AUTUMN:
            self.year = self.year + 1
            self.quarter = self.WINTER
        else:
            self.quarter = self.quarter + 1
        return self

    def previous(self):
        raise NotImplementedError()

    @property
    def name(self):
        return '{}{}'.format(self.QTR_NAMES.get(self.quarter), self.year)

    def _autumn_start_date(self, year):
        sept = datetime(year, 9, 24)
        return sept + relativedelta(weekday=2)  # last Wednesday

    def _winter_start_date(self, year):
        jan = datetime(year, 1, 2)
        # if Jan 1 is Sunday or Monday, start on Jan 3
        if jan.weekday() in [0, 1]:
            return jan.replace(day=3)
        return jan + relativedelta(weekday=0)  # first Monday after Jan 1

    def _spring_start_date(self, year):
        start = self._winter_start_date(year) + relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after winter

    def _summer_start_date(self, year):
        start = self._spring_start_date(year) + relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after spring

    def _term_from_datetime(self, dt: datetime):
        terms = [self._winter_start_date(dt.year),
                 self._spring_start_date(dt.year),
                 self._summer_start_date(dt.year),
                 self._autumn_start_date(dt.year)]

        quarter = 0
        while quarter < len(terms) and dt >= terms[quarter]:
            quarter += 1

        return dt.year, quarter if (quarter > 0) else self.AUTUMN


class ImportFileManager(models.Manager):
    pass


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    created_date = models.DateTimeField()
    processed_date = models.DateTimeField(null=True)
    processed_status = models.CharField(max_length=128, null=True)

    objects = ImportFileManager()

    def create_path(self, name):
        prefix = getattr(settings, 'FILENAME_PREFIX')
        if prefix is not None and len(prefix):
            name = '{}-{}'.format(prefix, name)

        if self.created_date is None:
            self.created_date = datetime.utcnow().replace(tzinfo=utc)

        self.path = self.created_date.strftime(
            '%Y/%m/%d/{}-%H%M%S.csv'.format(name))
        return self.path

    def sisimport(self):
        pass

    def create(self, academic_term):
        data = self.generate_csv(academic_term)
        write_file(self.create_path(academic_term.name), data)
        self.save()

    def generate_csv(self, academic_term):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.HANDSHAKE_CSV_HEADER)

        seen_uwnetids = set()
        for person in get_students_for_handshake(academic_term):
            if person.uwnetid in seen_uwnetids:
                continue

            if not valid_major_codes(person.student.majors):
                continue

            # TODO: don't write for students on requested account deletion list

            first_name, middle_name, last_name = format_name(person.first_name,
                                                             person.surname)

            writer.writerow([
                person.uwnetid,
                person.uwnetid,
                format_student_number(person.student.student_number),
                get_class_desc(person.student),
                last_name,
                first_name,
                middle_name,
                person.preferred_first_name,
                get_synced_college_name(person.student.majors),
                '{}@{}'.format(person.uwnetid, settings.EMAIL_DOMAIN),
                person.student.campus_desc,
                get_major_names(person.student.majors),
                get_primary_major_name(person.student.majors),
                'TRUE',
                # person.student.gender,
                # get_ethnicity_name(person.student.ethnicities),
                # is_athlete(person.student.special_program_code),
                # is_veteran(person.student.veteran_benefit_code),
                # 'work_study_eligible',  # TODO: get from visa type
                # 'primary_education:education_level_name',  # TODO: ?
            ])

            seen_uwnetids.add(person.uwnetid)

        return s.getvalue()
