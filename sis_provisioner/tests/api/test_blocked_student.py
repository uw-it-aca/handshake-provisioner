# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
import json
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from sis_provisioner.models.handshake import BlockedHandshakeStudent
from sis_provisioner.models.uconnect import BlockedUconnectStudent
from sis_provisioner.views.api.blocked_student import (
    HandshakeBlockedStudentListView,
    HandshakeBlockedStudentView,
    UconnectBlockedStudentListView,
    UconnectBlockedStudentView,
)


class HandshakeBlockedStudentListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')

    def _get(self):
        request = self.factory.get('/api/v1/handshake/blocked-student')
        request.user = self.user
        return HandshakeBlockedStudentListView.as_view()(request)

    def _post(self, body):
        request = self.factory.post(
            '/api/v1/handshake/blocked-student',
            data=json.dumps(body),
            content_type='application/json')
        request.user = self.user
        return HandshakeBlockedStudentListView.as_view()(request)

    def test_get_empty_list(self):
        response = self._get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_get_returns_students_ordered_by_added_date(self):
        t1 = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        t2 = datetime.datetime(2020, 6, 1, tzinfo=datetime.timezone.utc)
        BlockedHandshakeStudent.objects.create(
            username='astudent', added_by='admin', added_date=t1)
        BlockedHandshakeStudent.objects.create(
            username='bstudent', added_by='admin', added_date=t2)

        response = self._get()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        # Most recent first
        self.assertEqual(data[0]['username'], 'bstudent')
        self.assertEqual(data[1]['username'], 'astudent')

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_creates_blocked_student(self, mock_get_user):
        response = self._post({'student': {'username': 'javerage',
                                           'reason': 'Student request'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'javerage')
        self.assertEqual(data['reason'], 'Student request')
        self.assertEqual(data['added_by'], 'adminuser')
        self.assertTrue(
            BlockedHandshakeStudent.objects.filter(
                username='javerage').exists())

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_strips_and_lowercases_username(self, mock_get_user):
        response = self._post({'student': {'username': '  JAverage  ',
                                           'reason': 'Test'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'javerage')

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_duplicate_username_returns_existing(self, mock_get_user):
        added_date = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        existing = BlockedHandshakeStudent.objects.create(
            username='javerage', added_by='original', added_date=added_date,
            reason='Original reason')

        response = self._post({'student': {'username': 'javerage',
                                           'reason': 'New reason'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # get_or_create returns the existing record unchanged
        self.assertEqual(data['id'], existing.pk)
        self.assertEqual(data['added_by'], 'original')
        self.assertEqual(data['reason'], 'Original reason')
        self.assertEqual(BlockedHandshakeStudent.objects.count(), 1)

    def test_get_unauthenticated_redirects(self):
        request = self.factory.get('/api/v1/handshake/blocked-student')
        request.user = MagicMock(is_authenticated=False)
        response = HandshakeBlockedStudentListView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class HandshakeBlockedStudentViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')
        self.student = BlockedHandshakeStudent.objects.create(
            username='javerage',
            added_by='admin',
            added_date=datetime.datetime(
                2020, 1, 1, tzinfo=datetime.timezone.utc),
            reason='Test')

    def _delete(self, student_id):
        request = self.factory.delete(
            f'/api/v1/handshake/blocked-student/{student_id}')
        request.user = self.user
        return HandshakeBlockedStudentView.as_view()(
            request, student_id=student_id)

    def test_delete_removes_student_and_returns_204(self):
        response = self._delete(self.student.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            BlockedHandshakeStudent.objects.filter(
                pk=self.student.pk).exists())

    def test_delete_not_found_returns_404(self):
        response = self._delete(99999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_delete_unauthenticated_redirects(self):
        request = self.factory.delete(
            f'/api/v1/handshake/blocked-student/{self.student.pk}')
        request.user = MagicMock(is_authenticated=False)
        response = HandshakeBlockedStudentView.as_view()(
            request, student_id=self.student.pk)
        self.assertEqual(response.status_code, 302)


class UconnectBlockedStudentListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')

    def _get(self):
        request = self.factory.get('/api/v1/uconnect/blocked-student')
        request.user = self.user
        return UconnectBlockedStudentListView.as_view()(request)

    def _post(self, body):
        request = self.factory.post(
            '/api/v1/uconnect/blocked-student',
            data=json.dumps(body),
            content_type='application/json')
        request.user = self.user
        return UconnectBlockedStudentListView.as_view()(request)

    def test_get_empty_list(self):
        response = self._get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_get_returns_students_ordered_by_added_date(self):
        t1 = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        t2 = datetime.datetime(2020, 6, 1, tzinfo=datetime.timezone.utc)
        BlockedUconnectStudent.objects.create(
            username='astudent', added_by='admin', added_date=t1)
        BlockedUconnectStudent.objects.create(
            username='bstudent', added_by='admin', added_date=t2)

        response = self._get()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        # Most recent first
        self.assertEqual(data[0]['username'], 'bstudent')
        self.assertEqual(data[1]['username'], 'astudent')

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_creates_blocked_student(self, mock_get_user):
        response = self._post({'student': {'username': 'javerage',
                                           'reason': 'Student request'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'javerage')
        self.assertEqual(data['reason'], 'Student request')
        self.assertEqual(data['added_by'], 'adminuser')
        self.assertTrue(
            BlockedUconnectStudent.objects.filter(
                username='javerage').exists())

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_strips_and_lowercases_username(self, mock_get_user):
        response = self._post({'student': {'username': '  JAverage  ',
                                           'reason': 'Test'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'javerage')

    @patch('sis_provisioner.views.api.blocked_student.get_user',
           return_value='adminuser')
    def test_post_duplicate_username_returns_existing(self, mock_get_user):
        added_date = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        existing = BlockedUconnectStudent.objects.create(
            username='javerage', added_by='original', added_date=added_date,
            reason='Original reason')

        response = self._post({'student': {'username': 'javerage',
                                           'reason': 'New reason'}})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['id'], existing.pk)
        self.assertEqual(data['added_by'], 'original')
        self.assertEqual(data['reason'], 'Original reason')
        self.assertEqual(BlockedUconnectStudent.objects.count(), 1)

    def test_get_unauthenticated_redirects(self):
        request = self.factory.get('/api/v1/uconnect/blocked-student')
        request.user = MagicMock(is_authenticated=False)
        response = UconnectBlockedStudentListView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class UconnectBlockedStudentViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser')
        self.student = BlockedUconnectStudent.objects.create(
            username='javerage',
            added_by='admin',
            added_date=datetime.datetime(
                2020, 1, 1, tzinfo=datetime.timezone.utc),
            reason='Test')

    def _delete(self, student_id):
        request = self.factory.delete(
            f'/api/v1/uconnect/blocked-student/{student_id}')
        request.user = self.user
        return UconnectBlockedStudentView.as_view()(
            request, student_id=student_id)

    def test_delete_removes_student_and_returns_204(self):
        response = self._delete(self.student.pk)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            BlockedUconnectStudent.objects.filter(
                pk=self.student.pk).exists())

    def test_delete_not_found_returns_404(self):
        response = self._delete(99999)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_delete_unauthenticated_redirects(self):
        request = self.factory.delete(
            f'/api/v1/uconnect/blocked-student/{self.student.pk}')
        request.user = MagicMock(is_authenticated=False)
        response = UconnectBlockedStudentView.as_view()(
            request, student_id=self.student.pk)
        self.assertEqual(response.status_code, 302)
