# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings


def valid_class_code(class_code):
    return class_code in getattr(settings, 'INCLUDED_CLASS_CODES', [])


def valid_campus_code(campus_code):
    return campus_code in getattr(settings, 'INCLUDED_CAMPUS_CODES', [])


def valid_major_codes(majors):
    excluded_codes = getattr(settings, 'EXCLUDED_MAJOR_CODES', [])
    for major in majors:
        if major.major_abbr_code in excluded_codes:
            return False
    return True


def is_athlete(special_program_code):
    athlete_codes = getattr(settings, 'ATHLETE_CODES', [])
    return special_program_code in athlete_codes


def is_veteran(veteran_benefit_code):
    return veteran_benefit_code != '0'


def get_college_for_major(major):
    if major.major_abbr_code in getattr(settings, 'ENGR_COLLEGE_MAJORS', []):
        return 'J'
    return major.college


def get_synced_college_code(codes):
    return max(codes) if codes else None


def get_major_names(majors):
    return ','.join([m.major_name for m in majors])


def get_synced_college_name(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    college_dict = getattr(settings, 'COLLEGES', {})
    return college_dict.get(college_code, None)
