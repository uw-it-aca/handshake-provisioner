# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.dao.student import (
    HandshakePersonClient, get_students_for_handshake)
import mock


class StudentDAOFunctionsTest(TestCase):
    @mock.patch.object(HandshakePersonClient, 'get_registered_students')
    @mock.patch('sis_provisioner.dao.student.current_next_terms')
    def test_get_students_for_handshake(self, mock_terms,
                                        mock_get_registered_students):
        years = [2022]
        quarters = [1, 2]
        mock_terms.return_value = (years, quarters)

        r = get_students_for_handshake()
        mock_get_registered_students.assert_called_with(
            include_employee=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_intended_majors=False,
            include_student_pending_majors=False,
            include_student_requested_majors=False,
            include_term_years=years,
            include_term_quarters=quarters)
