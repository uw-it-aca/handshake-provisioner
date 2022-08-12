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

    def test_valid_major_codes(self):
        excluded_major = self._build_major(major_abbr_code='0-GEMBA')
        major = self._build_major(major_abbr_code='1')
        major2 = self._build_major(major_abbr_code='2')
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
        major = self._build_major(major_abbr_code='0-BSE', college='C')
        self.assertEqual(get_college_for_major(major), 'J')
        major.major_abbr_code = '2'
        major.college = 'S'
        self.assertEqual(get_college_for_major(major), 'S')

    def test_get_synced_college_code(self):
        codes = ['A', 'B', 'C']
        self.assertEqual(get_synced_college_code(codes), 'C')
        self.assertEqual(get_synced_college_code(None), None)

    def test_get_major_names(self):
        major = self._build_major(major_abbr_code='0-BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')
        student1 = self._build_student(majors=[major, major2])
        student2 = self._build_student(majors=[])
        student3 = self._build_student(majors=[major])
        student4 = self._build_student(majors=[major3])
        student5 = self._build_student(majors=[major, major3])
        student6 = self._build_student(majors=[], pending_majors=[major])
        student7 = self._build_student(majors=[major], pending_majors=[major3],
                                       requested_majors=[major2])
        student8 = self._build_student(majors=[major], pending_majors=[major3],
                                       requested_majors=[major],
                                       intended_majors=[major2])

        self.assertEqual(get_major_names(student1),
                         'Bachelor of Science;Master of Science')
        self.assertEqual(get_major_names(student2), '')
        self.assertEqual(get_major_names(student3), 'Bachelor of Science')
        self.assertEqual(get_major_names(student4), '')
        self.assertEqual(get_major_names(student5),
                         'Bachelor of Science;Business Administration')
        self.assertEqual(get_major_names(student6), 'Bachelor of Science')
        self.assertEqual(get_major_names(student7),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')
        self.assertEqual(get_major_names(student8),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')

    def test_get_synced_college_name(self):
        major = self._build_major(major_abbr_code='0-BSE', college='C')
        major2 = self._build_major(major_abbr_code='2', college='S')
        major3 = self._build_major(major_abbr_code='3', college='C')
        major4 = self._build_major(major_abbr_code='0-CSE', college='C')

        student1 = self._build_student(majors=[major])
        student2 = self._build_student(majors=[major2])
        student3 = self._build_student(majors=[major3])
        student4 = self._build_student(majors=[major, major2])
        student5 = self._build_student(majors=[major, major3])
        student6 = self._build_student(majors=[major3, major2])
        student7 = self._build_student(majors=[major, major2, major3])
        student8 = self._build_student(majors=[major4, major2, major3])
        student9 = self._build_student(majors=[major, major2, major4])
        student10 = self._build_student(majors=[major, major4, major3])
        student11 = self._build_student(majors=[major, major2, major4, major3])
        student12 = self._build_student(majors=[])

        self.assertEqual(get_synced_college_name(student1),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name(student2),
                         'The Information School')
        self.assertEqual(get_synced_college_name(student3),
                         'College of Arts & Sciences')
        self.assertEqual(get_synced_college_name(student4),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name(student5),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name(student6),
                         'The Information School')
        self.assertEqual(get_synced_college_name(student7),
                         'College of Engineering')
        self.assertEqual(get_synced_college_name(student8),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name(student9),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name(student10),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name(student11),
                         'School of Computer Science & Engineering')
        self.assertEqual(get_synced_college_name(student12), None)

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

        student = self._build_student(class_code='1', majors=[major1])

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
