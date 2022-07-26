# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from sis_provisioner.dao.file import read_file, write_file
from sis_provisioner.dao.student import get_students_for_handshake
from sis_provisioner.utils import (
    valid_major_codes, get_major_names, get_primary_major_name, is_athlete,
    is_veteran, get_synced_college_name, get_ethnicity_name,
    current_next_terms)
from datetime import datetime
import csv
import io


class ImportFileManager(models.Manager):
    pass


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True)
    processed_status = models.CharField(max_length=128, null=True)

    objects = ImportFileManager()

    def sisimport(self):
        pass

    def create(self):
        self.path = datetime.now().strftime('%Y/%m/%d/%H%M%S-%f.csv')
        write_file(self.path, self.generate_csv())
        self.save()

    def generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.HANDSHAKE_CSV_HEADER)

        for person in get_students_for_handshake(current_next_terms()):
            if not valid_major_codes(person.student.majors):
                continue

            writer.writerow([
                person.uwnetid,
                person.uwnetid,
                person.student.student_number,
                person.student.class_desc,
                person.surname,
                person.first_name,
                person.preferred_middle_name,
                person.preferred_first_name,
                get_synced_college_name(person.student.majors),
                person.student.student_email,
                person.student.campus_desc,
                get_major_names(person.student.majors),
                get_primary_major_name(person.student.majors),
                'TRUE',  # TODO: primary_education:currently_attending
                # person.student.gender,
                # get_ethnicity_name(person.student.ethnicities),
                # is_athlete(person.student.special_program_code),
                # is_veteran(person.student.veteran_benefit_code),
                # 'work_study_eligible',  # TODO: get from visa type
                # 'primary_education:education_level_name',  # TODO: ?
            ])

        return s.getvalue()
