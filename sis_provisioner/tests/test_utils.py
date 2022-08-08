# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from uw_person_client.components import Major, Student
from sis_provisioner.utils import *


@override_settings()
class HandshakeUtilsTest(TestCase):
    def test_valid_major_codes(self):
        excluded_major = Major()
        excluded_major.major_abbr_code = '0-GEMBA'
        major = Major()
        major.major_abbr_code = '1'
        major2 = Major()
        major2.major_abbr_code = '2'
        majors_1 = [major, excluded_major]
        majors_2 = [major, major2]
        self.assertFalse(valid_major_codes(majors_1))
        self.assertTrue(valid_major_codes(majors_2))

    def test_is_athlete(self):
        self.assertTrue(is_athlete('30'))
        self.assertFalse(is_athlete('13'))
        self.assertFalse(is_athlete(25))

    def test_is_veteran(self):
        self.assertTrue(is_veteran('1'))
        self.assertFalse(is_veteran('0'))

    def test_get_college_for_major(self):
        major = Major()
        major.major_abbr_code = '0-BSE'
        major.college = 'C'
        self.assertEqual(get_college_for_major(major), 'J')
        major.major_abbr_code = '2'
        major.college = 'S'
        self.assertEqual(get_college_for_major(major), 'S')

    def test_get_synced_college_code(self):
        codes = ['A', 'B', 'C']
        self.assertEqual(get_synced_college_code(codes), 'C')
        self.assertEqual(get_synced_college_code(None), None)

    def test_get_major_names(self):
        major = Major()
        major.major_full_name = 'Bachelor of Science'
        major.college = 'F'
        major.major_abbr_code = '0-BSE'
        major2 = Major()
        major2.major_full_name = 'Master of Science'
        major2.college = 'A'
        major2.major_abbr_code = '1'
        major3 = Major()
        major3.major_full_name = 'Business Administration'
        major3.college = 'E'
        major3.major_abbr_code = '2'
        self.assertEqual(get_major_names([major, major2]),
                         'Bachelor of Science;Master of Science')
        self.assertEqual(get_major_names([]), '')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')
        self.assertEqual(get_major_names([major3]), '')
        self.assertEqual(get_major_names([major, major3]),
                         'Bachelor of Science;Business Administration')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')

    def test_get_synced_college_name(self):
        major = Major()
        major.major_abbr_code = '0-BSE'
        major.college = 'C'
        major2 = Major()
        major2.major_abbr_code = '2'
        major2.college = 'S'
        major3 = Major()
        major3.major_abbr_code = '3'
        major3.college = 'C'
        self.assertEqual(get_synced_college_name([major, major2]),
                         'The Information School')
        self.assertEqual(get_synced_college_name([major, major3]),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name([major3]),
                         'College of Arts & Sciences')
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
        major1 = Major()
        major1.major_abbr_code = '0'
        major1.college = 'C'
        major2 = Major()
        major2.major_abbr_code = '0-EMBA'
        major2.college = 'E'
        major3 = Major()
        major3.major_abbr_code = '0-EMBA'
        major3.college = 'F'

        student = Student()
        student.class_code = '1'
        student.majors = [major1]

        self.assertEqual(get_class_desc(student), 'Freshman')
        student.class_code = '2'
        self.assertEqual(get_class_desc(student), 'Sophomore')
        student.class_code = '3'
        self.assertEqual(get_class_desc(student), 'Junior')
        student.class_code = '4'
        self.assertEqual(get_class_desc(student), 'Senior')
        student.class_code = '5'
        self.assertEqual(get_class_desc(student), 'Senior')
        student.class_code = '8'
        self.assertEqual(get_class_desc(student), 'Masters')
        student.majors = [major2]
        self.assertEqual(get_class_desc(student),
                         'Masters of Business Administration')
        student.majors = [major2, major3]
        self.assertEqual(get_class_desc(student),
                         'Masters')
        student.majors = [major1, major2]
        self.assertEqual(get_class_desc(student),
                         'Masters of Business Administration')
        student.class_code = '9'
        self.assertEqual(get_class_desc(student), None)
        student.class_code = 1
        self.assertEqual(get_class_desc(student), None)

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

    def test_format_first_name(self):
        self.assertEqual(format_first_name('John Doe'), ('John', 'Doe'))
        self.assertEqual(format_first_name('John Doe Jr'), ('John', 'Doe Jr'))
        self.assertEqual(format_first_name('JOHN ROY'), ('John', 'Roy'))
        self.assertEqual(format_first_name('JOHN ROY S'), ('John', 'Roy S'))
        self.assertEqual(format_first_name('John    Doe'), ('John', 'Doe'))
        self.assertEqual(format_first_name('John '), ('John', ''))
        self.assertEqual(format_first_name('JOHN '), ('John', ''))
        self.assertEqual(format_first_name(' John '), ('John', ''))
        self.assertEqual(format_first_name('John'), ('John', ''))
        self.assertEqual(format_first_name(''), ('', ''))
        self.assertEqual(format_first_name(None), ('', ''))

    def test_format_last_name(self):
        self.assertEqual(format_last_name('Smith'), 'Smith')
        self.assertEqual(format_last_name('Smith-Jones'), 'Smith-Jones')
        self.assertEqual(format_last_name('SMITH JONES'), 'Smith Jones')
        self.assertEqual(format_last_name('SMITH III'), 'Smith III')
        self.assertEqual(format_last_name('SMITH'), 'Smith')
        self.assertEqual(format_last_name('Smith '), 'Smith')
        self.assertEqual(format_last_name('SMITH '), 'Smith')
        self.assertEqual(format_last_name(' Smith '), 'Smith')
        self.assertEqual(format_last_name(' '), '')
        self.assertEqual(format_last_name(None), '')
