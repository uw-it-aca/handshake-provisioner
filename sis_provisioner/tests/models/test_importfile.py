# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.models import ImportFile
from datetime import datetime


class ImportFileTest(TestCase):
    @override_settings(FILENAME_PREFIX=None)
    def test_create_path(self):
        impfile = ImportFile()
        name = 'AUT2019'

        impfile.created_date = datetime(2019, 6, 15, 2, 45, 0)
        self.assertEqual(impfile.create_path(name),
                         '2019/06/15/AUT2019-024500.csv')

    @override_settings(FILENAME_PREFIX='TEST')
    def test_create_path_prefix(self):
        impfile = ImportFile()
        name = 'AUT2019'

        impfile.created_date = datetime(2019, 6, 15, 2, 45, 0)
        self.assertEqual(impfile.create_path(name),
                         '2019/06/15/TEST-AUT2019-024500.csv')
