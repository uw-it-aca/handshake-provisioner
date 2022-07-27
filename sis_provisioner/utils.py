# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from datetime import datetime
import re


RE_WORD_BOUNDS = re.compile(r'(\s|-|\(|\)|\.|,|/|:|&|")')
RE_UNTITLEIZE = re.compile(r'^(?:And|For|Of|The|W)$')
RE_TITLE_ABBR = re.compile(r'^(?:Bs|Ms)$')


def cap_first_letter(string):
    if len(string) < 2:
        return string.upper()
    return string[0].upper() + string[1:]


def titleize(string, andrepl='and'):
    if string is None:
        raise TypeError('String is required')

    titled_string = ''

    for word in re.split(RE_WORD_BOUNDS, str(string)):
        titled_string += re.sub(
            RE_UNTITLEIZE, lambda m: m.group(0).lower(), word.capitalize()
        )

    new_titled_string = ''

    for word in re.split(RE_WORD_BOUNDS, str(titled_string)):
        new_titled_string += re.sub(
            RE_TITLE_ABBR, lambda m: m.group(0).upper(), word
        )

    return cap_first_letter(new_titled_string.replace(' and ', f' {andrepl} '))


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


def get_majors(majors):
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
