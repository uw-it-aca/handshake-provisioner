# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_person_client import UWPersonClient


class HandshakePersonClient(UWPersonClient):
    def get_registered_students(self, term_years, term_quarters, **kwargs):
        sqla_persons = self.DB.session.query(self.DB.Person).join(
            self.DB.Student).join(
            self.DB.Term, self.DB.Student.academic_term).filter(
                self.DB.Student.enroll_status_code == settings.ENROLL_STATUS,
                self.DB.Student.campus_code.in_(settings.INCLUDE_CAMPUS_CODES),
                self.DB.Student.class_code.in_(settings.INCLUDE_CLASS_CODES),
                self.DB.Term.year.in_(term_years),
                self.DB.Term.quarter.in_(term_quarters)
            )
        return [self._map_person(p, **kwargs) for p in sqla_persons.all()]


def get_students_for_handshake(term_years, term_quarters):
    return HandshakePersonClient().get_registered_students(
        term_years, term_quarters,
        include_employee=False,
        include_student_transcripts=False,
        include_student_transfers=False,
        include_student_sports=False,
        include_student_advisers=False,
        include_student_intended_majors=False,
        include_student_pending_majors=False,
        include_student_requested_majors=False)
