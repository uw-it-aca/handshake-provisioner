# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from sis_provisioner.dao.student import *
from sis_provisioner.models.term import Term


class StudentTest(TestCase):
    databases = '__all__'
    fixtures = ['person.json', 'employee.json', 'term.json', 'major.json',
                'student.json', 'adviser.json', 'transfer.json',
                'transcript.json', 'hold.json', 'degree.json', 'sport.json']

    def test_get_students_for_handshake(self):
        term = Term(year=2013, quarter=3)
        students = get_students_for_handshake(term)
        self.assertEqual(len(students), 2)
        # print(students.query)

    def test_get_students_for_uconnect(self):
        term = Term(year=2013, quarter=3)
        students = get_students_for_uconnect(term)
        self.assertEqual(len(students), 2)

    def test_get_active_students(self):
        students = get_active_students()
        self.assertEqual(len(students), 2)

    def test_get_majors(self):
        majors = get_majors_by_code(['PSOCS', 'SIS'])
        self.assertEqual(len(majors), 0)
