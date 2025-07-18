# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from uw_person_client.models import Student, Major
from sis_provisioner.utils import *


class HandshakeUtilsTest(TestCase):
    def _build_major(self, major_abbr_code=None, college=None,
                     major_full_name=None, major_pathway=None):
        major = Major()
        major.major_abbr_code = major_abbr_code
        major.college = college
        major.major_full_name = major_full_name
        major.major_pathway = major_pathway
        return major

    def _build_student(self, majors=[], pending_majors=[], requested_majors=[],
                       intended_majors=[], class_code=None,
                       enroll_status_code=12, application_status_code=16,
                       special_program_code=None, veteran_benefit_code=None):
        student = Student()
        student.majors = majors
        student.pending_majors = pending_majors
        if requested_majors:
            for i in range(3):
                code = None
                if len(requested_majors) > i:
                    code = requested_majors[i].major_abbr_code
                setattr(student, f'requested_major{i+1}_code', code)
        if intended_majors:
            for i in range(3):
                setattr(student, f'intended_major{i+1}_code',
                        intended_majors[i].major_abbr_code)
                if len(intended_majors) == i:
                    break
        student.class_code = class_code
        student.enroll_status_code = enroll_status_code
        student.application_status_code = application_status_code
        student.special_program_code = special_program_code
        student.veteran_benefit_code = veteran_benefit_code
        return student

    def test_get_majors(self):
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
        major11 = self._build_major(
            major_abbr_code='EDUC I', major_full_name='Education Certificate',
            college='H')

        student = self._build_student(majors=[major2])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major8, major2])
        self.assertEqual(len(get_majors(student)), 1)

        student = self._build_student(majors=[major1, major2, major3])
        self.assertEqual(len(get_majors(student)), 3)

        student = self._build_student(majors=[major8, major1, major2])
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
        student = self._build_student(special_program_code='30')
        self.assertTrue(is_athlete(student))

        student = self._build_student(special_program_code='13')
        self.assertFalse(is_athlete(student))

        student = self._build_student(special_program_code='25')
        self.assertTrue(is_athlete(student))

    def test_is_veteran(self):
        student = self._build_student(veteran_benefit_code=1)
        self.assertTrue(is_veteran(student))

        student = self._build_student(veteran_benefit_code=0)
        self.assertFalse(is_veteran(student))

    def test_get_college_for_major(self):
        major = self._build_major(major_abbr_code='BSE', college='C')
        self.assertEqual(get_college_for_major(major), 'J')
        major.major_abbr_code = '2'
        major.college = 'S'
        self.assertEqual(get_college_for_major(major), 'S')

    def test_get_major_names(self):
        major = self._build_major(major_abbr_code='BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')
        major4 = self._build_major(major_abbr_code='ACCTG', college='E',
                                   major_full_name='Business Administration',
                                   major_pathway='1')
        major5 = self._build_major(major_abbr_code='CISB', college='E',
                                   major_full_name='Business Administration',
                                   major_pathway='0')

        self.assertEqual(get_major_names([major, major2]),
                         'Bachelor of Science;Master of Science')
        self.assertEqual(get_major_names([]), '')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')
        self.assertEqual(get_major_names([major3]), 'Business Administration')
        self.assertEqual(get_major_names([major4]),
                         'Business Administration (Accounting) - UW Seattle')
        self.assertEqual(get_major_names([major, major3]),
                         'Bachelor of Science;Business Administration')
        self.assertEqual(get_major_names([major, major4]),
                         'Bachelor of Science;'
                         'Business Administration (Accounting) - UW Seattle')
        self.assertEqual(get_major_names([major]), 'Bachelor of Science')
        self.assertEqual(get_major_names([major, major3, major2]),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')
        self.assertEqual(get_major_names([major, major3, major2]),
                         'Bachelor of Science;Business Administration;'
                         'Master of Science')
        self.assertEqual(
            get_major_names([major5]),
            'Business Administration (Certificate in International Business)')

    def test_get_primary_major_name(self):
        major = self._build_major(major_abbr_code='BSE', college='F',
                                  major_full_name='Bachelor of Science')
        major2 = self._build_major(major_abbr_code='1', college='A',
                                   major_full_name='Master of Science')
        major3 = self._build_major(major_abbr_code='2', college='E',
                                   major_full_name='Business Administration')
        major4 = self._build_major(major_abbr_code='MST', college='E',
                                   major_full_name='Business Administration',
                                   major_pathway='0')

        self.assertEqual(get_primary_major_name([major, major2]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([]), '')
        self.assertEqual(get_primary_major_name([major]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([major3]),
                         'Business Administration')
        self.assertEqual(get_primary_major_name([major4]),
                         'Master of Science in Taxation')
        self.assertEqual(get_primary_major_name([major, major3]),
                         'Bachelor of Science')
        self.assertEqual(get_primary_major_name([major, major4, major2]),
                         'Bachelor of Science')
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

        self.assertFalse(is_excluded_college(major.college))
        self.assertFalse(is_excluded_college(major2.college))
        self.assertFalse(is_excluded_college(major3.college))

    def test_get_college_names(self):
        major = self._build_major(major_abbr_code='BSE', college='C')
        major2 = self._build_major(major_abbr_code='2', college='S')
        major3 = self._build_major(major_abbr_code='3', college='C')
        major4 = self._build_major(major_abbr_code='CSE', college='C')
        major5 = self._build_major(major_abbr_code='BIOEN', college='O')

        self.assertEqual(get_college_names([major]),
                         'College of Engineering')
        self.assertEqual(get_college_names([major2]),
                         'The Information School')
        self.assertEqual(get_college_names([major3]),
                         'College of Arts & Sciences')
        self.assertEqual(get_college_names([major2, major]),
                         'The Information School;College of Engineering')
        self.assertEqual(get_college_names([major, major3]),
                         'College of Engineering;College of Arts & Sciences')
        self.assertEqual(get_college_names([major2, major3]),
                         'The Information School;College of Arts & Sciences')
        self.assertEqual(get_college_names(
            [major4, major2, major3]), (
            'School of Computer Science & Engineering;'
            'The Information School;College of Arts & Sciences'))
        self.assertEqual(
            get_college_names([major4, major2]),
            'School of Computer Science & Engineering;The Information School')
        self.assertEqual(get_college_names(
            [major4, major2, major, major3]), (
            'School of Computer Science & Engineering;The Information School;'
            'College of Engineering;College of Arts & Sciences'))
        self.assertEqual(get_college_names([major5]),
                         'College of Engineering')
        self.assertEqual(get_college_names([]), '')
        self.assertEqual(get_college_names([], campus=1), 'UW Bothell')

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

        student = self._build_student(class_code=1)
        self.assertEqual(get_class_desc(student, [major1]), 'Freshman')
        student = self._build_student(class_code=2)
        self.assertEqual(get_class_desc(student, [major1]), 'Sophomore')
        student = self._build_student(class_code=3)
        self.assertEqual(get_class_desc(student, [major1]), 'Junior')
        student = self._build_student(class_code=4)
        self.assertEqual(get_class_desc(student, [major1]), 'Senior')
        student = self._build_student(class_code=5)
        self.assertEqual(get_class_desc(student, [major1]), 'Senior')
        student = self._build_student(class_code=6)
        self.assertEqual(get_class_desc(student, [major1]), None)
        student = self._build_student(class_code=8)
        self.assertEqual(get_class_desc(student, [major1]), 'Masters')

        student = self._build_student(class_code=1)
        self.assertEqual(get_class_desc(student, [major2]),
                         'Masters of Business Administration')
        student = self._build_student(class_code=8)
        self.assertEqual(get_class_desc(student, [major2, major3]),
                         'Masters of Business Administration')
        student = self._build_student(class_code=8)
        self.assertEqual(get_class_desc(student, [major1, major2]),
                         'Masters of Business Administration')
        student = self._build_student(class_code=9)
        self.assertEqual(get_class_desc(student, [major1, major2]), None)

    def test_get_education_level_name(self):
        student = self._build_student(class_code=9)
        self.assertEqual(get_education_level_name(student), None)

        student = self._build_student(class_code=2)
        self.assertEqual(get_education_level_name(student), 'Bachelors')

        student = self._build_student(class_code=8)
        self.assertEqual(get_education_level_name(student), 'Masters')

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
