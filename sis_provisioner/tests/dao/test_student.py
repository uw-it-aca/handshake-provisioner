# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.dao.student import (
    HandshakePersonClient, get_students_for_handshake)
import mock


class StudentDAOFunctionsTest(TestCase):
    @mock.patch.object(HandshakePersonClient, 'get_registered_students')
    def test_get_students_for_handshake(self, mock_get_registered_students):
        academic_terms = [(2022, 4), (2023, 1)]

        r = get_students_for_handshake(academic_terms)
        mock_get_registered_students.assert_called_with(
            academic_terms,
            include_employee=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_intended_majors=True,
            include_student_pending_majors=True,
            include_student_requested_majors=True)
