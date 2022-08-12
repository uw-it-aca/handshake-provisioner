# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from nameparser import HumanName
import re

RE_WORD_BOUNDS = re.compile(r'(\s|-|\(|\)|\.|,|/|:|&|")')
RE_UNTITLEIZE = re.compile(r'^(?:and|for|of|the|w)$', re.I)
RE_TITLE_ABBR = re.compile(r'^(?:bs|ms)$', re.I)

STUDENT_NUM_LEN = 7


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


def is_athlete(special_program_code):
    athlete_codes = getattr(settings, 'ATHLETE_CODES', [])
    return special_program_code in athlete_codes


def is_veteran(veteran_benefit_code):
    return veteran_benefit_code != '0'


def get_class_desc(class_code, majors):
    if class_code not in getattr(settings, 'INCLUDE_CLASS_CODES', []):
        return None

    if (any('MBA' in major.major_abbr_code for major in majors) and
            get_synced_college_name(majors) == 'Foster School of Business'):
        return 'Masters of Business Administration'
    return getattr(settings, 'CLASS_CODES', {}).get(class_code, None)


def format_student_number(number):
    return number.zfill(STUDENT_NUM_LEN)


def get_college_for_major(major):
    if major.major_abbr_code in getattr(settings, 'ENGR_COLLEGE_MAJORS', []):
        return 'J'
    if major.major_abbr_code in getattr(settings, 'CSE_COLLEGE_MAJORS', []):
        return 'J2'
    return major.college


def get_synced_college_code(codes):
    if not codes:
        return None
    if 'J2' in codes:
        return 'J2'
    if 'J' in codes:
        return 'J'
    return max(codes)


def is_no_sync_college(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    return college_code == 'E' or college_code == 'V'


def get_majors(student):
    excluded_codes = getattr(settings, 'EXCLUDE_MAJOR_CODES', [])
    majors = {}
    for major in (student.majors + student.pending_majors +
                  student.requested_majors + student.intended_majors):
        # remove duplicates, skipping the excluded majors
        if major.major_abbr_code not in excluded_codes:
            majors[major.major_abbr_code] = major
    return majors.values()


def get_major_names(majors):
    if not is_no_sync_college(majors):
        return ';'.join([m.major_full_name for m in majors])
    return ''


def get_primary_major_name(majors):
    if len(majors) and not is_no_sync_college(majors):
        return majors[0].major_full_name


def get_synced_college_name(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    college_dict = getattr(settings, 'COLLEGES', {})
    return college_dict.get(college_code)


def get_ethnicity_name(ethnicities):
    try:
        return ethnicities[0].assigned_ethnic_desc
    except (IndexError, AttributeError):
        pass


def format_name(first_name, surname):
    try:
        full_name = ' '.join([first_name, surname])
    except TypeError:
        full_name = first_name or surname or ''

    hname = HumanName(full_name)
    hname.capitalize(force=True)
    last = re.sub('^[a-z]', lambda x: x.group().upper(), hname.last)
    return hname.first, hname.middle, (last + ' ' + hname.suffix).strip()
