# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_person_client.models import Person, Major, Q
from sis_provisioner.exceptions import EmptyQueryException


def get_students_for_handshake(academic_term):
    next_academic_term = academic_term.next()

    persons = Person.objects.using('uw_person').filter(
        Q(
            student__academic_term__year=academic_term.year,
            student__academic_term__quarter=academic_term.quarter) |
        Q(
            student__academic_term__year=next_academic_term.year,
            student__academic_term__quarter=next_academic_term.quarter),
        student__campus_code__in(settings.INCLUDE_CAMPUS_CODES),
        Q(
            student__enroll_status_code=settings.ENROLLED_STATUS,
            student__class_code__in(settings.ENROLLED_CLASS_CODES)) |
        Q(
            student__application_status_code=settings.APPLICANT_STATUS,
            student__class_code__in(settings.APPLICANT_CLASS_CODES),
            student__application_type_code__in(list(
                settings.APPLICANT_TYPES.values())))
        ).prefetch_related('student_set')

    if not persons:
        raise EmptyQueryException()
    return persons


def get_active_students():
    return Person.objects.using('uw_person').get_active_students()


def get_majors_by_code(codes: list):
    return Major.objects.using('uw_person').filter(
        major_abbr_code__in(codes), major_pathway=0).exclude(
        major_full_name='').exclude(
        major_full_name__isnull=True).exclude(
        major_last_yr__isnull=True)
