# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client import UWPersonClient


def get_students_for_handshake():
    return UWPersonClient().get_registered_students(
        include_employee=False,
        include_student_transcripts=False,
        include_student_transfers=False,
        include_student_sports=False,
        include_student_advisers=False,
        include_student_intended_majors=False,
        include_student_pending_majors=False,
        include_student_requested_majors=False)
