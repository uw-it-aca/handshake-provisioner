# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from sis_provisioner.views.api.file.uconnect import (
    UconnectFileListView, UconnectFileView)
from sis_provisioner.models.uconnect import UconnectStudentsFile
from sis_provisioner.models.term import Term
import datetime
import json


class UconnectFileListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')
        self.term = Term(year=2020, quarter=Term.AUTUMN)
        self.term.save()

    def _get(self):
        request = self.factory.get('/api/v1/uconnect/file')
        request.user = self.user
        return UconnectFileListView.as_view()(request)

    def _post(self, body):
        request = self.factory.post(
            '/api/v1/uconnect/file',
            data=json.dumps(body),
            content_type='application/json')
        request.user = self.user
        return UconnectFileListView.as_view()(request)

    def test_get_empty_list(self):
        response = self._get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_get_returns_files_ordered_by_created_date(self):
        t1 = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        t2 = datetime.datetime(2020, 6, 1, tzinfo=datetime.timezone.utc)
        UconnectStudentsFile.objects.create(
            term=self.term, created_date=t1)
        UconnectStudentsFile.objects.create(
            term=self.term, created_date=t2)

        response = self._get()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        # Most recent first
        self.assertEqual(data[0]['created_date'], t2.isoformat())
        self.assertEqual(data[1]['created_date'], t1.isoformat())

    @patch('sis_provisioner.views.api.file.uconnect.get_user',
           return_value='testuser')
    @patch('sis_provisioner.views.api.file.uconnect.Term')
    def test_post_current_term(self, mock_term_class, mock_get_user):
        mock_term_class.objects.current.return_value = self.term
        response = self._post({'file': {'academic_term': 'current',
                                        'is_test_file': True}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['is_test_file'], True)
        self.assertEqual(data['created_by'], 'testuser')
        mock_term_class.objects.current.assert_called_once()

    @patch('sis_provisioner.views.api.file.uconnect.get_user',
           return_value='testuser')
    @patch('sis_provisioner.views.api.file.uconnect.Term')
    def test_post_next_term(self, mock_term_class, mock_get_user):
        mock_term_class.objects.next.return_value = self.term
        response = self._post({'file': {'academic_term': 'next',
                                        'is_test_file': False}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['is_test_file'], False)
        mock_term_class.objects.next.assert_called_once()

    def test_post_invalid_term_returns_400(self):
        response = self._post({'file': {'academic_term': 'invalid'}})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_post_missing_term_returns_400(self):
        response = self._post({'file': {}})
        self.assertEqual(response.status_code, 400)

    def test_get_unauthenticated_redirects(self):
        request = self.factory.get('/api/v1/uconnect/file')
        request.user = MagicMock(is_authenticated=False)
        response = UconnectFileListView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class UconnectFileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')
        self.term = Term(year=2020, quarter=Term.AUTUMN)
        self.term.save()
        self.import_file = UconnectStudentsFile.objects.create(
            term=self.term,
            created_date=datetime.datetime(
                2020, 10, 1, tzinfo=datetime.timezone.utc))

    def _get(self, file_id):
        request = self.factory.get(f'/api/v1/uconnect/file/{file_id}')
        request.user = self.user
        return UconnectFileView.as_view()(request, file_id=file_id)

    def _put(self, file_id):
        request = self.factory.put(f'/api/v1/uconnect/file/{file_id}')
        request.user = self.user
        return UconnectFileView.as_view()(request, file_id=file_id)

    def _delete(self, file_id):
        request = self.factory.delete(f'/api/v1/uconnect/file/{file_id}')
        request.user = self.user
        return UconnectFileView.as_view()(request, file_id=file_id)

    # --- GET ---

    def test_get_returns_file_content(self):
        with patch.object(UconnectStudentsFile, 'content',
                          new_callable=lambda: property(
                              lambda self: 'username,email\njaverage,j@uw.edu'
                          )):
            self.import_file.generated_date = datetime.datetime(
                2020, 10, 2, tzinfo=datetime.timezone.utc)
            self.import_file.save()
            response = self._get(self.import_file.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])

    def test_get_file_not_found_returns_404(self):
        response = self._get(99999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_get_file_not_available_returns_404(self):
        with patch.object(UconnectStudentsFile, 'content',
                          new_callable=lambda: property(
                              fget=lambda self: (_ for _ in ()).throw(
                                  FileNotFoundError())
                          )):
            self.import_file.generated_date = datetime.datetime(
                2020, 10, 2, tzinfo=datetime.timezone.utc)
            self.import_file.save()
            response = self._get(self.import_file.pk)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Not Available')

    # --- PUT ---

    def test_put_calls_sisimport_and_returns_json(self):
        with patch.object(UconnectStudentsFile, 'sisimport') as mock_import:
            response = self._put(self.import_file.pk)
        self.assertEqual(response.status_code, 200)
        mock_import.assert_called_once()
        data = json.loads(response.content)
        self.assertEqual(data['id'], self.import_file.pk)

    def test_put_file_not_found_returns_404(self):
        response = self._put(99999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_put_file_not_available_returns_404(self):
        with patch.object(UconnectStudentsFile, 'sisimport',
                          side_effect=FileNotFoundError):
            response = self._put(self.import_file.pk)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Not Available')

    def test_put_generic_exception_returns_500(self):
        with patch.object(UconnectStudentsFile, 'sisimport',
                          side_effect=Exception('something went wrong')):
            response = self._put(self.import_file.pk)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertIn('error', data)

    # --- DELETE ---

    def test_delete_removes_file_and_returns_204(self):
        response = self._delete(self.import_file.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            UconnectStudentsFile.objects.filter(
                pk=self.import_file.pk).exists())

    def test_delete_file_not_found_returns_404(self):
        response = self._delete(99999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_delete_file_not_available_returns_404(self):
        with patch.object(UconnectStudentsFile, 'delete',
                          side_effect=FileNotFoundError):
            response = self._delete(self.import_file.pk)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Not Available')
