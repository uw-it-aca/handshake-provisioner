# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from uw_person_client.components import Major, Student
from sis_provisioner.utils import *


@override_settings()
class HandshakeUtilsTest(TestCase):
    def _build_major(self, major_abbr_code=None, college=None,
                     major_full_name=None):
        major = Major()
        major.major_abbr_code = major_abbr_code
        major.college = college
        major.major_full_name = major_full_name
        return major

    def _build_student(self, majors=[], pending_majors=[], requested_majors=[],
                       intended_majors=[], class_code=None):
        student = Student()
        student.majors = majors
        student.pending_majors = pending_majors
        student.requested_majors = requested_majors
        student.intended_majors = intended_majors
        student.class_code = class_code
        return student

    def test_get_majors(self):
        major0 = self._build_major(
            major_abbr_code='GEMBA', major_full_name='Major 0', college='J')
        major1 = self._build_major(
            major_abbr_code='A', major_full_name='Major 1', college='A1')
        major2 = self._build_major(
            major_abbr_code='B', major_full_name='Major 2', college='B2')
        major3 = self._build_major(
            major_abbr_code='C', major_full_name='Major 3', college='C3')
        major4 = self._build_major(
            major_abbr_code='D', major_full_name=None, college='D4')
        major5 = self._build_major(
            major_abbr_code='E', major_full_name='Major 5', college=None)

        student = self._build_student(majors=[major0])
        self.assertEqual(len(get_majors(student)), 0)

        student = self._build_student(pending_majors=[major2])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(requested_majors=[major2])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major0, major2])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major1, major2, major3])
        self.assertEqual(len(get_majors(student)), 3)

        student = self._build_student(majors=[major0, major1, major2])
        self.assertEqual(len(get_majors(student)), 2)

        student = self._build_student(majors=[major1, major2, major4])
        self.assertEqual(len(get_majors(student)), 2)

        student = self._build_student(majors=[major1, major4, major5])
        self.assertEqual(len(get_majors(student)), 1)

    def test_is_athlete(self):
        self.assertTrue(is_athlete('30'))
        self.assertFalse(is_athlete('13'))
        self.assertFalse(is_athlete(25))

    def test_is_veteran(self):
        self.assertTrue(is_veteran('1'))
        self.assertFalse(is_veteran('0'))

    def test_get_college_for_major(self):
        major = self._build_major(major_abbr_code='BSE', college='C')
        self.assertEqual(get_college_for_major(major), 'J')
        major.major_abbr_code = '2'
        major.college = 'S'
        self.assertEqual(get_college_for_major(major), 'S')

    def test_get_synced_college_code(self):
        codes = ['A', 'B', 'C']
        self.assertEqual(get_synced_college_code(codes), 'C')
        self.assertEqual(get_synced_college_code(None), None)

    def test_get_major_names(self):
        major = self._build_major(major_abbr_code='BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')

        self.assertEqual(get_major_names([major, major2]),
                         'Bachelor of Science;Master of Science')
        self.assertEqual(get_major_names([]), '')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')
        self.assertEqual(get_major_names([major3]), '')
        self.assertEqual(get_major_names([major, major3]),
                         'Bachelor of Science;Business Administration')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')
        self.assertEqual(get_major_names([major, major3, major2]),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')
        self.assertEqual(get_major_names([major, major3, major2]),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')

    def test_get_synced_college_name(self):
        major = self._build_major(major_abbr_code='BSE', college='C')
        major2 = self._build_major(major_abbr_code='2', college='S')
        major3 = self._build_major(major_abbr_code='3', college='C')
        major4 = self._build_major(major_abbr_code='CSE', college='C')

        self.assertEqual(get_synced_college_name([major]),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name([major2]),
                         'The Information School')
        self.assertEqual(get_synced_college_name([major3]),
                         'College of Arts & Sciences')
        self.assertEqual(get_synced_college_name([major, major2]),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name([major, major3]),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name([major3, major2]),
                         'The Information School')
        self.assertEqual(get_synced_college_name([major, major2, major3]),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name([major4, major2, major3]),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name([major, major2, major4]),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name([major, major4, major3]),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name(
            [major, major2, major4, major3]),
            'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name([]), None)

    def test_titleize(self):
        self.assertRaises(TypeError, titleize, None)
        self.assertEqual(titleize(123), '123')
        self.assertEqual(titleize(''), '')
        self.assertEqual(titleize('bachelor of science'),
                         'Bachelor of Science')
        self.assertEqual(titleize('arts and sciences', andrepl='&'),
                         'Arts & Sciences')
        self.assertEqual(titleize('arts and sciences'), 'Arts and Sciences')
        self.assertEqual(titleize('It\'s for majors'), 'It\'s for Majors')
        self.assertEqual(titleize('The INFORMATION (hi) school'),
                         'The Information (Hi) School')
        self.assertEqual(titleize('special school (w/ honors)'),
                         'Special School (w/ Honors)')
        self.assertEqual(titleize('and, (,for,) '), 'And, (,for,)')
        self.assertEqual(titleize('foR ,BS/JS/,MS'), 'For ,BS/Js/,MS')
        self.assertEqual(titleize('He said "hi"'), 'He Said "Hi"')
        self.assertEqual(titleize('computers,science,and engineering (BS/MS)'),
                         'Computers,Science,and Engineering (BS/MS)'),
        self.assertEqual(titleize('waffles &, and w/syrup', andrepl='&'),
                         'Waffles &, & w/Syrup')
        self.assertEqual(titleize('a new, improved title'),
                         'A New, Improved Title')
        self.assertEqual(titleize(' a new, improved title '),
                         'A New, Improved Title')

    def test_get_class_desc(self):
        major1 = self._build_major(major_abbr_code='0', college='C')
        major2 = self._build_major(major_abbr_code='0-EMBA', college='E')
        major3 = self._build_major(major_abbr_code='0-EMBA', college='F')

        majors = [major1]
        self.assertEqual(get_class_desc('1', majors), 'Freshman')
        self.assertEqual(get_class_desc('2', majors), 'Sophomore')
        self.assertEqual(get_class_desc('3', majors), 'Junior')
        self.assertEqual(get_class_desc('4', majors), 'Senior')
        self.assertEqual(get_class_desc('5', majors), 'Senior')
        self.assertEqual(get_class_desc('8', majors), 'Masters')

        majors = [major2]
        self.assertEqual(get_class_desc('8', majors),
                         'Masters of Business Administration')
        majors = [major2, major3]
        self.assertEqual(get_class_desc('8', majors), 'Masters')

        majors = [major1, major2]
        self.assertEqual(get_class_desc('8', majors),
                         'Masters of Business Administration')
        self.assertEqual(get_class_desc('9', majors), None)
        self.assertEqual(get_class_desc(1, majors), None)

    def test_format_student_number(self):
        self.assertEqual(format_student_number('1234567'), '1234567')
        self.assertEqual(format_student_number('123456'), '0123456')
        self.assertEqual(format_student_number('12345'), '0012345')
        self.assertEqual(format_student_number('1234'), '0001234')
        self.assertEqual(format_student_number('123'), '0000123')
        self.assertEqual(format_student_number('12'), '0000012')
        self.assertEqual(format_student_number('1'), '0000001')
        self.assertEqual(format_student_number(''), '0000000')
        self.assertRaises(AttributeError, format_student_number, 1234567)

    def test_format_name(self):
        self.assertEqual(format_name('John ', 'Doe'), ('John', '', 'Doe'))
        self.assertEqual(format_name('John', 'Doe Jr'), ('John', '', 'Doe Jr'))
        self.assertEqual(format_name('JOHN', 'ROY'), ('John', '', 'Roy'))
        self.assertEqual(format_name('JOHN JAMES', 'ROY Sr'),
                         ('John', 'James', 'Roy Sr'))
        self.assertEqual(format_name('Michael', 'Three-names Butcher III'),
                         ('Michael', 'Three-Names', 'Butcher III'))
        self.assertEqual(format_name(' Jon Q ', ' Doe '), ('Jon', 'Q', 'Doe'))
        self.assertEqual(format_name(' ', ''), ('', '', ''))
        self.assertEqual(format_name(None, ''), ('', '', ''))
        self.assertEqual(format_name('', None), ('', '', ''))
        self.assertEqual(format_name(None, None), ('', '', ''))
        self.assertEqual(format_name(0, 0), ('', '', ''))
        self.assertEqual(format_name('Leland M', 'McDonald'),
                         ('Leland', 'M', 'McDonald'))
        self.assertEqual(format_name('Joe', 'Le'), ('Joe', '', 'Le'))
