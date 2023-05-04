# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase, override_settings
from sis_provisioner.dao.student import (
    HandshakePersonClient, get_students_for_handshake, get_active_students)
from sis_provisioner.exceptions import EmptyQueryException
from sis_provisioner.models import Term
import mock


class StudentDAOFunctionsTest(TestCase):
    @mock.patch.object(HandshakePersonClient, 'get_registered_students')
    def test_get_students_for_handshake(self, mock_get_registered_students):
        academic_term = Term(year=2013, quarter=1)

        mock_get_registered_students.return_value = [{}]
        r = get_students_for_handshake(academic_term)
        mock_get_registered_students.assert_called_with(
            academic_term,
            include_employee=False,
            include_student=True,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_majors=True,
            include_student_pending_majors=True,
            include_student_holds=False)

        mock_get_registered_students.return_value = []
        self.assertRaises(EmptyQueryException, get_students_for_handshake,
                          academic_term)

    @mock.patch.object(HandshakePersonClient, 'get_active_students')
    def test_get_active_students(self, mock_get_active_students):
        r = get_active_students()
        mock_get_active_students.assert_called_with(
            include_employee=False,
            include_student=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_majors=False,
            include_student_pending_majors=False,
            include_student_holds=False)
