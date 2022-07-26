# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.dao.student import (
    HandshakePersonClient, get_students_for_handshake)
import mock


class StudentDAOFunctionsTest(TestCase):
    @mock.patch.object(HandshakePersonClient, 'get_registered_students')
    def test_get_students_for_handshake(self, mock_get_registered_students):
        term_years = [2022]
        term_quarters = [1, 2]

        r = get_students_for_handshake(term_years, term_quarters)
        mock_get_registered_students.assert_called_with(
            term_years, term_quarters,
            include_employee=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_intended_majors=False,
            include_student_pending_majors=False,
            include_student_requested_majors=False)
