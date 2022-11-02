# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from uw_person_client.components import Ethnicity, Major, Student
from sis_provisioner.utils import *


class HandshakeUtilsTest(TestCase):
    def _build_major(self, major_abbr_code=None, college=None,
                     major_full_name=None):
        major = Major()
        major.major_abbr_code = major_abbr_code
        major.college = college
        major.major_full_name = major_full_name
        return major

    def _build_student(self, majors=[], pending_majors=[], requested_majors=[],
                       intended_majors=[], class_code=None,
                       enroll_status_code='12', application_status_code='16'):
        student = Student()
        student.majors = majors
        student.pending_majors = pending_majors
        student.requested_majors = requested_majors
        student.intended_majors = intended_majors
        student.class_code = class_code
        student.enroll_status_code = enroll_status_code
        student.application_status_code = application_status_code
        return student

    def _build_ethnicity(self, ethnic_code=None, ethnic_desc=None,
                         group_desc=None):
        ethnicity = Ethnicity()
        ethnicity.assigned_ethnic_code = ethnic_code
        ethnicity.assigned_ethnic_desc = ethnic_desc
        ethnicity.assigned_ethnic_group_desc = group_desc
        return ethnicity

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
        major6 = self._build_major(
            major_abbr_code='PREMJR', major_full_name='Major 6', college='G')
        major7 = self._build_major(
            major_abbr_code='F', major_full_name='Undeclared Major 7',
            college='J')
        major8 = self._build_major(
            major_abbr_code='N MATR', major_full_name='Unmatriculated Major 8',
            college='J')
        major9 = self._build_major(
            major_abbr_code='PSOCS', major_full_name='Premajor 9', college='J')
        major10 = self._build_major(
            major_abbr_code='HI', major_full_name='Major 10', college='J')

        student = self._build_student(majors=[major0])
        self.assertEqual(len(get_majors(student)), 0)

        student = self._build_student(majors=[major2])
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

        student = self._build_student(majors=[major2, major6])
        self.assertEqual(len(get_majors(student)), 2)

        student = self._build_student(majors=[major9, major10])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major6])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major6, major7])
        self.assertEqual(len(get_majors(student)), 2)

        student = self._build_student(majors=[major6, major9])
        self.assertEqual(len(get_majors(student)), 2)

        student = self._build_student(majors=[major7])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major8])
        self.assertEqual(len(get_majors(student)), 0)

        student = self._build_student(majors=[major6, major8])
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

    def test_get_college_code(self):
        codes = ['A', 'B', 'C']
        self.assertEqual(get_college_code(codes), 'C')
        self.assertEqual(get_college_code([]), None)
        self.assertEqual(get_college_code(['V']), None)
        self.assertEqual(get_college_code(['V'] + codes), 'C')
        self.assertEqual(get_college_code(['V', 'Z']), None)
        self.assertEqual(get_college_code(['C', 'Z']), 'C')
        self.assertEqual(get_college_code(['Y', 'J2']), 'J2')

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

    def test_get_primary_major_name(self):
        major = self._build_major(major_abbr_code='BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')

        self.assertEqual(get_primary_major_name([major, major2]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([]), None)
        self.assertEqual(get_primary_major_name([major]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([major3]), None)
        self.assertEqual(get_primary_major_name([major, major3]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([major, major3, major2]),
                         'Bachelor of Science')
        major3.college = 'F'
        self.assertEqual(get_primary_major_name([major3, major2]),
                         'Business Administration')
        self.assertEqual(get_primary_major_name([major2]), 'Master of Science')

    def test_is_excluded_college(self):
        major = self._build_major(major_abbr_code='BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')

        self.assertFalse(is_excluded_college([major, major2]))
        self.assertTrue(is_excluded_college([]))
        self.assertFalse(is_excluded_college([major]))
        self.assertTrue(is_excluded_college([major3]))
        self.assertFalse(is_excluded_college([major, major3]))
        self.assertFalse(is_excluded_college([major, major3, major2]))
        major3.college = 'F'
        self.assertFalse(is_excluded_college([major3, major2]))

    def test_get_college_name(self):
        major = self._build_major(major_abbr_code='BSE', college='C')
        major2 = self._build_major(major_abbr_code='2', college='S')
        major3 = self._build_major(major_abbr_code='3', college='C')
        major4 = self._build_major(major_abbr_code='CSE', college='C')

        self.assertEqual(get_college_name([major]),
                         'College of Engineering')
        self.assertEqual(get_college_name([major2]),
                         'The Information School')
        self.assertEqual(get_college_name([major3]),
                         'College of Arts & Sciences')
        self.assertEqual(get_college_name([major2, major]),
                         'The Information School')
        self.assertEqual(get_college_name([major, major3]),
                         'College of Engineering')
        self.assertEqual(get_college_name([major2, major3]),
                         'The Information School')
        self.assertEqual(get_college_name([major2, major, major3]),
                         'The Information School')
        self.assertEqual(get_college_name([major4, major2, major3]),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_college_name([major4, major2]),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_college_name(
            [major4, major2, major, major3]),
            'School of Computer Science & Engineering')
        self.assertEqual(get_college_name([]), None)
        self.assertEqual(get_college_name([], campus='1'), 'UW Bothell')

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

        student = self._build_student(class_code='1')
        self.assertEqual(get_class_desc(student, [major1]), 'Freshman')
        student = self._build_student(class_code='2')
        self.assertEqual(get_class_desc(student, [major1]), 'Sophomore')
        student = self._build_student(class_code='3')
        self.assertEqual(get_class_desc(student, [major1]), 'Junior')
        student = self._build_student(class_code='4')
        self.assertEqual(get_class_desc(student, [major1]), 'Senior')
        student = self._build_student(class_code='5')
        self.assertEqual(get_class_desc(student, [major1]), 'Senior')
        student = self._build_student(class_code='6')
        self.assertEqual(get_class_desc(student, [major1]), None)
        student = self._build_student(class_code='8')
        self.assertEqual(get_class_desc(student, [major1]), 'Masters')

        student = self._build_student(class_code='1')
        self.assertEqual(get_class_desc(student, [major2]),
                         'Masters of Business Administration')
        student = self._build_student(class_code='8')
        self.assertEqual(get_class_desc(student, [major2, major3]),
                         'Masters of Business Administration')
        student = self._build_student(class_code='8')
        self.assertEqual(get_class_desc(student, [major1, major2]),
                         'Masters of Business Administration')

        student = self._build_student(class_code='9')
        self.assertEqual(get_class_desc(student, [major1, major2]), None)
        student = self._build_student(class_code=1)
        self.assertEqual(get_class_desc(student, [major1, major2]), None)

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

    def test_get_ethnicity_name(self):
        ethnicity1 = self._build_ethnicity(ethnic_desc='Vietnamese')
        ethnicity2 = self._build_ethnicity(ethnic_desc='French')
        ethnicity3 = self._build_ethnicity(ethnic_desc='Turkish')

        self.assertEqual(get_ethnicity_name([ethnicity1]), 'Vietnamese')
        self.assertEqual(get_ethnicity_name([ethnicity2]), 'French')
        self.assertEqual(get_ethnicity_name([ethnicity3]), 'Turkish')
        self.assertEqual(get_ethnicity_name([ethnicity3, ethnicity1]),
                         'Turkish')
        self.assertEqual(get_ethnicity_name([ethnicity2, ethnicity1]),
                         'French')
        self.assertEqual(get_ethnicity_name([]), None)
        self.assertEqual(get_ethnicity_name(
            [ethnicity1, ethnicity2, ethnicity3]), 'Vietnamese')
