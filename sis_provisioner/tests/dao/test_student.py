# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.dao.student import UWHandshakeClient


@override_settings()
class StudentDAOFunctionsTest(TestCase):
    def test_valid_class_code(self):
        self.assertTrue(UWHandshakeClient.valid_class_code('1'))
        self.assertFalse(UWHandshakeClient.valid_class_code('0'))
        self.assertFalse(UWHandshakeClient.valid_class_code(1))

    def test_valid_campus_code(self):
        pass

    def test_valid_major_code(self):
        pass
