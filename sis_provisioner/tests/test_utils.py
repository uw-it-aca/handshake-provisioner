# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.utils import *


@override_settings()
class StudentDAOFunctionsTest(TestCase):
    def test_valid_class_code(self):
        self.assertTrue(valid_class_code('1'))
        self.assertTrue(valid_class_code('5'))
        self.assertFalse(valid_class_code('0'))
        self.assertFalse(valid_class_code(1))

    def test_valid_campus_code(self):
        self.assertTrue(valid_campus_code('0'))
        self.assertFalse(valid_campus_code('2'))
        self.assertFalse(valid_campus_code(1))

    def test_valid_major_codes(self):
        pass
