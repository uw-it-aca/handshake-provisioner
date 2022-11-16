# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.models import (
    HandshakeStudentsFile, ActiveStudentsFile, Term)
import datetime


class HandshakeStudentsFileTest(TestCase):
    def setUp(self):
        term = Term(year=2019, quarter=4)
        term.save()
        self.term = term
        self.created_date = datetime.datetime(
            2019, 6, 15, 2, 45, 0, tzinfo=datetime.timezone.utc)

    @override_settings(FILENAME_TEST_PREFIX=None)
    def test_create_path(self):
        impfile = HandshakeStudentsFile(term=self.term,
                                        created_date=self.created_date)
        impfile.save()

        self.assertEqual(impfile.filename, 'AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.path,
                         '2019/06/AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.json_data(), {
            'api_path': ('/api/v1/file/1',),
            'created_by': 'automatic',
            'created_date': '2019-06-15T02:45:00+00:00',
            'generated_date': None,
            'id': 1,
            'import_progress': 0,
            'imported_date': None,
            'imported_status': None,
            'is_test_file': False,
            'name': 'AUT2019-20190615-024500.csv',
            'process_id': None,
            'term': {'id': 1, 'quarter': 'AUT', 'year': 2019}
        })

    @override_settings(FILENAME_TEST_PREFIX='TEST')
    def test_create_path_prefix(self):
        impfile = HandshakeStudentsFile(
            term=self.term, is_test_file=True, created_date=self.created_date)
        impfile.save()

        self.assertEqual(impfile.filename, 'TEST-AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.path,
                         '2019/06/TEST-AUT2019-20190615-024500.csv')
        self.assertEqual(impfile.json_data(), {
            'api_path': ('/api/v1/file/1',),
            'created_by': 'automatic',
            'created_date': '2019-06-15T02:45:00+00:00',
            'generated_date': None,
            'id': 1,
            'import_progress': 0,
            'imported_date': None,
            'imported_status': None,
            'is_test_file': True,
            'name': 'TEST-AUT2019-20190615-024500.csv',
            'process_id': None,
            'term': {'id': 1, 'quarter': 'AUT', 'year': 2019}
        })


class ActiveStudentsFileTest(TestCase):
    def setUp(self):
        self.created_date = datetime.datetime(
            2019, 6, 15, 2, 45, 0, tzinfo=datetime.timezone.utc)

    def test_create_path(self):
        impfile = ActiveStudentsFile(created_date=self.created_date)
        impfile.save()

        self.assertEqual(impfile.filename,
                         'active-students-20190615-024500.csv')
        self.assertEqual(impfile.path,
                         '2019/06/active-students-20190615-024500.csv')
        self.assertEqual(impfile.json_data(), {
            'created_by': 'automatic',
            'created_date': '2019-06-15T02:45:00+00:00',
            'generated_date': None,
            'id': 1,
            'import_progress': 0,
            'imported_date': None,
            'imported_status': None,
            'name': 'active-students-20190615-024500.csv',
            'process_id': None
        })
