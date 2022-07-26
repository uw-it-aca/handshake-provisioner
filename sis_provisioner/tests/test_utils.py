# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from uw_person_client.components import Major
from sis_provisioner.utils import *


@override_settings()
class HandshakeUtilsTest(TestCase):
    def test_current_next_terms(self):
        pass

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
        major.college = 'C'
        major2 = Major()
        major2.major_name = 'Master of Science'
        major2.college = 'A'
        self.assertEqual(get_major_names([major, major2]),
                         'Bachelor Of Science;Master Of Science')
        self.assertEqual(get_major_names([]), '')
        self.assertEqual(get_major_names([major]), 'Bachelor Of Science')

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
                         'College Of Engineering')
        self.assertEqual(get_synced_college_name([major3]),
                         'College Of Arts And Sciences')
        self.assertEqual(get_synced_college_name([]), None)
