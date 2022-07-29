# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from uw_person_client.components import Major
from sis_provisioner.utils import *
from mock import patch


@override_settings()
class HandshakeUtilsTest(TestCase):
    def test_valid_major_codes(self):
        excluded_major = Major()
        excluded_major.major_abbr_code = '0-EMBA'
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
        major.major_name = 'Bachelor of Science'
        major.college = 'F'
        major.major_abbr_code = '0-BSE'
        major2 = Major()
        major2.major_name = 'Master of Science'
        major2.college = 'A'
        major2.major_abbr_code = '1'
        major3 = Major()
        major3.major_name = 'Business Administration'
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
        self.assertEquals(titleize(''), '')
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

    def test_get_current_next_term(self):
        term = DateToTerm()
        with patch('sis_provisioner.utils.datetime') as mock_datetime:
            mock_datetime.side_effect = datetime
            mock_datetime.now.return_value = datetime(2020, 1, 31)
            self.assertEqual(term.current_next_terms(),
                             [(2020, 1), (2020, 2)])
            mock_datetime.now.return_value = datetime(2020, 12, 31)
            self.assertEqual(term.current_next_terms(),
                             [(2020, 4), (2021, 1)])
            mock_datetime.now.return_value = datetime(2020, 2, 29)
            self.assertEqual(term.current_next_terms(),
                             [(2020, 1), (2020, 2)])
            mock_datetime.now.return_value = datetime(2020, 5, 15)
            self.assertEqual(term.current_next_terms(),
                             [(2020, 2), (2020, 3)])
            mock_datetime.now.return_value = datetime(2020, 9, 15)
            self.assertEqual(term.current_next_terms(),
                             [(2020, 3), (2020, 4)])

    def test_get_quarter_from_date(self):
        term = DateToTerm()
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 1, 1)), 4)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 4, 1)), 2)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2021, 6, 20)), 2)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2021, 6, 21)), 3)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 10, 1)), 4)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 1, 3, 1, 0)), 1)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 4, 1, 1, 0)), 2)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 6, 20, 1, 0)), 3)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 10, 1, 1, 0)), 4)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 1, 2, 1, 0)), 4)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 4, 1, 1, 0)), 2)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 9, 27, 1, 0)), 3)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 9, 28, 1, 0)), 4)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 3, 27)), 1)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2022, 3, 28)), 2)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2020, 7, 1, 2, 0)), 3)
        self.assertEqual(
            term.get_quarter_from_date(datetime(2023, 6, 20, 2, 0)), 3)