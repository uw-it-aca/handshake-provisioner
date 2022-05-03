# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from sis_provisioner.dao.file import read_file, write_file


@override_settings(MEDIA_ROOT='/app')
class FileDAOFunctionsTest(TestCase):
    def setUp(self):
        self.test_data = b'This is a test str.'
        self.test_path = 'test.txt'

        with default_storage.open(self.test_path, mode='wb') as f:
            f.write(self.test_data)

    def test_read_file(self):
        self.assertEqual(read_file(self.test_path).encode(), self.test_data)
        self.assertRaises(ObjectDoesNotExist, read_file, 'test.csv')

    def test_write_file(self):
        new_data = b'New test data'
        write_file(self.test_path, new_data)
        self.assertEqual(read_file(self.test_path).encode(), new_data)
