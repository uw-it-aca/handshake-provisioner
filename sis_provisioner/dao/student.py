# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from sqlalchemy import or_, and_
from uw_person_client import UWPersonClient
from sis_provisioner.exceptions import EmptyQueryException


class HandshakePersonClient(UWPersonClient):
    def get_registered_students(self, academic_term, **kwargs):
        next_academic_term = academic_term.next()
        Person = self.DB.Person
        Student = self.DB.Student
        Term = self.DB.Term
        sqla_persons = self.DB.session.query(Person).join(Student).join(
            Term, Student.academic_term).filter(
                or_(and_(
                        Term.year == academic_term.year,
                        Term.quarter == academic_term.quarter),
                    and_(
                        Term.year == next_academic_term.year,
                        Term.quarter == next_academic_term.quarter)),
                Student.campus_code.in_(settings.INCLUDE_CAMPUS_CODES),
                or_(and_(
                        Student.enroll_status_code == settings.ENROLLED_STATUS,
                        Student.class_code.in_(settings.ENROLLED_CLASS_CODES)),
                    and_(
                        Student.application_status_code == settings.APPLICANT_STATUS,  # noqa
                        Student.class_code.in_(settings.APPLICANT_CLASS_CODES)))  # noqa
            )
        return [self._map_person(p, **kwargs) for p in sqla_persons.all()]

    def get_requested_majors(self, abbr_codes: list):
        sqla_majors = self.DB.session.query(self.DB.Major).filter(
            self.DB.Major.major_abbr_code.in_(abbr_codes),
            self.DB.Major.major_pathway == 0,
            self.DB.Major.major_full_name != '',
            self.DB.Major.major_full_name.is_not(None),
            self.DB.Major.major_last_yr.is_not(None),
        )
        return [self._map_major(m) for m in sqla_majors.all()]

    def get_active_students(self, **kwargs):
        sqla_persons = self.DB.session.query(self.DB.Person).filter(
            self.DB.Person._is_active_student == True  # noqa
        )
        return [self._map_person(p, **kwargs) for p in sqla_persons.all()]


def get_students_for_handshake(academic_term):
    kwargs = {
        'include_employee': False,
        'include_student': True,
        'include_student_transcripts': False,
        'include_student_transfers': False,
        'include_student_sports': False,
        'include_student_advisers': False,
        'include_student_majors': True,
        'include_student_pending_majors': True,
    }
    client = HandshakePersonClient()
    students = client.get_registered_students(academic_term, **kwargs)
    if not len(students):
        raise EmptyQueryException()
    return students


def get_majors_by_code(codes: list):
    client = HandshakePersonClient()
    return client.get_requested_majors(codes)


def get_active_students():
    kwargs = {
        'include_employee': False,
        'include_student': False,
        'include_student_transcripts': False,
        'include_student_transfers': False,
        'include_student_sports': False,
        'include_student_advisers': False,
        'include_student_majors': False,
        'include_student_pending_majors': False,
    }
    client = HandshakePersonClient()
    return client.get_active_students(**kwargs)
