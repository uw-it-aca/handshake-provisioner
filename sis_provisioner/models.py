# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from sis_provisioner.dao.file import read_file, write_file
from sis_provisioner.dao.student import get_students_for_handshake
from sis_provisioner.utils import (
    valid_class_code, valid_campus_code, valid_major_codes,
    get_college_for_major, get_major_names)
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
        s = io.BytesIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.HANDSHAKE_CSV_HEADER)

        for person in get_students_for_handshake():
            if not valid_class_code(person.student.class_code):
                continue

            if not valid_campus_code(person.student.campus_code):
                continue

            if not valid_major_codes(person.student.majors):
                continue

            writer.writerow([
                person.uwnetid,
                person.student.student_email,
                person.student.student_number,
                person.student.class_code,  # TODO: year name
                person.student.campus_code,  # TODO: campus name
                person.last_name,
                person.first_name,
                person.preferred_middle_name,
                person.preferred_first_name,
                get_college_for_major(person.student.majors[0]),  # TODO: name
                get_major_names(person.student.majors),
                person.student.gender,
                person.assigned_ethnic_code,  # TODO: letter code?
                'athlete',  # TODO: true|false?
                person.student.veteran_benefit_code,  # TODO: true|false?
                'work_study_eligible',
                'primary_education:education_level_name',  # TODO: ?
            ])

        return s
