# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_person_client.models import Person, Student, Major, Q
from sis_provisioner.exceptions import EmptyQueryException
from logging import getLogger

logger = getLogger(__name__)


def get_students_for_handshake(academic_term):
    next_academic_term = academic_term.next()
    autumn_year_qtr_id = str(academic_term.year) + str(academic_term.AUTUMN)

    enrolled_queryset = Student.objects.filter(
            campus_code__in=settings.INCLUDE_CAMPUS_CODES,
            enroll_status_code=settings.ENROLLED_STATUS,
            class_code__in=settings.ENROLLED_CLASS_CODES
        ).filter(
            (Q(academic_term__year=academic_term.year) &
                Q(academic_term__quarter=academic_term.quarter)) |
            (Q(academic_term__year=next_academic_term.year) &
                Q(academic_term__quarter=next_academic_term.quarter))
        )

    applicant_queryset = Student.objects.filter(
            campus_code__in=settings.INCLUDE_CAMPUS_CODES,
            application_status_code=settings.APPLICANT_STATUS,
            application_type_code__in=list(settings.APPLICANT_TYPES.values()),
            class_code__in=settings.APPLICANT_CLASS_CODES,
            admitted_for_yr_qtr_id=autumn_year_qtr_id
        )

    queryset = enrolled_queryset | applicant_queryset

    if not queryset:
        raise EmptyQueryException()
    return queryset


def get_active_students():
    return Person.objects.get_active_students()


def get_majors_by_code(codes: list):
    return Major.objects.filter(
        major_abbr_code__in(codes), major_pathway=0).exclude(
        major_full_name='').exclude(
        major_full_name__isnull=True).exclude(
        major_last_yr__isnull=True)
