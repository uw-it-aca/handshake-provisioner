# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.models import ImportFile, Term
from datetime import datetime


class ImportFileTest(TestCase):
    def setUp(self):
        term = Term(year=2019, quarter=4)
        term.save()
        self.term = term

    @override_settings(FILENAME_PREFIX=None)
    def test_create_path(self):
        impfile = ImportFile(term=self.term)

        impfile.created_date = datetime(2019, 6, 15, 2, 45, 0)
        self.assertEqual(impfile.create_path(),
                         '2019/06/AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.filename, 'AUT2019-20190615-024500.csv')

    @override_settings(FILENAME_PREFIX='TEST')
    def test_create_path_prefix(self):
        impfile = ImportFile(term=self.term, is_test_file=True)

        impfile.created_date = datetime(2019, 6, 15, 2, 45, 0)
        self.assertEqual(impfile.create_path(),
                         '2019/06/TEST-AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.filename, 'TEST-AUT2019-20190615-024500.csv')
