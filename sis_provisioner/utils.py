# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from datetime import datetime
import re

RE_WORD_BOUNDS = re.compile(r'(\s|-|\(|\)|\.|,|/|:|&|")')
RE_UNTITLEIZE = re.compile(r'^(?:and|for|of|the|w)$', re.I)
RE_TITLE_ABBR = re.compile(r'^(?:bs|ms)$', re.I)


def titleize(string, andrepl='and'):
    """
    Capitalizes the first letter of every word, effective only in ASCII region.
    """
    if string is None:
        raise TypeError('String is required')

    titled_string = ''

    for idx, word in enumerate(re.split(RE_WORD_BOUNDS, str(string).strip())):
        if re.match(RE_TITLE_ABBR, word):
            titled_string += word.upper()

        elif re.match(RE_UNTITLEIZE, word):
            word = word.lower().replace('and', andrepl)
            titled_string += word.capitalize() if (idx == 0) else word

        else:
            titled_string += word.capitalize()

    return titled_string


def current_next_terms():
    return [(2022, 3), (2022, 4)]  # TODO: ...


def valid_major_codes(majors):
    excluded_codes = getattr(settings, 'EXCLUDE_MAJOR_CODES', [])
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


def is_no_sync_college(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    return college_code == 'E' or college_code == 'V'


def get_majors(majors):
    if is_no_sync_college(majors):
        return []
    majors.sort(key=lambda m: m.college, reverse=True)
    return majors


def get_major_names(majors):
    majors = get_majors(majors)
    return ';'.join([titleize(m.major_name) for m in majors])


def get_primary_major_name(majors):
    majors = get_majors(majors)
    try:
        return titleize(majors[0].major_name)
    except IndexError:
        pass


def get_synced_college_name(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    college_dict = getattr(settings, 'COLLEGES', {})
    try:
        return titleize(college_dict.get(college_code), andrepl='&')
    except (AttributeError, TypeError):
        pass


def get_ethnicity_name(ethnicities):
    try:
        return titleize(ethnicities[0].assigned_ethnic_desc)
    except IndexError:
        pass
