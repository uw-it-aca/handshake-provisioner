# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from sis_provisioner.dao.student import get_majors_by_code
from nameparser import HumanName
from logging import getLogger
import re

RE_WORD_BOUNDS = re.compile(r'(\s|-|\(|\)|\.|,|/|:|&|")')
RE_UNTITLEIZE = re.compile(r'^(?:and|for|of|the|w)$', re.I)
RE_TITLE_ABBR = re.compile(r'^(?:bs|ms)$', re.I)

STUDENT_NUM_LEN = 7

logger = getLogger(__name__)


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


def get_class_desc(student, majors):
    class_code = student.class_code
    if (student.enroll_status_code != settings.ENROLLED_STATUS and
            student.application_status_code == settings.APPLICANT_STATUS):
        class_code = getattr(settings, 'APPLICANT_TYPES', {}).get(
            student.application_type_desc, class_code)

    if class_code not in getattr(settings, 'ENROLLED_CLASS_CODES', []):
        return None

    if (any('MBA' in major.major_abbr_code and major.college == 'E'
            for major in majors)):
        return 'Masters of Business Administration'

    return getattr(settings, 'CLASS_CODES', {}).get(class_code)


def format_student_number(number):
    return number.zfill(STUDENT_NUM_LEN)


def get_college_for_major(major):
    return getattr(settings, 'MAJOR_COLLEGE_OVERRIDES', {}).get(
        major.major_abbr_code, major.college)


def get_synced_college_code(codes: list):
    if not codes:
        return None
    if 'J2' in codes:
        return 'J2'
    return max(codes)


def is_no_sync_college(majors):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    return college_code == 'E' or college_code == 'V'


def get_requested_majors(student):
    requested = [
        student.requested_major1_code,
        student.requested_major2_code,
        student.requested_major3_code
    ]
    # filter out empty codes
    codes = [code for code in requested if code]
    if len(codes):
        return get_majors_by_code(codes)
    return []


def is_pre_major(major):
    return (
        'PRE' in major.major_abbr_code or
        'Undeclared' in major.major_full_name or
        major.major_abbr_code in getattr(settings, 'PRE_MAJOR_CODES', []))


def is_excluded_major(major):
    return major.major_abbr_code in getattr(
        settings, 'EXCLUDE_MAJOR_CODES', [])


def validate_majors(majors) -> list:
    cleaned_majors = []
    for major in majors:
        if major.major_full_name is None or major.college is None:
            logger.warning('MISSING data for major: {}'.format(
                major.major_abbr_code))
        else:
            cleaned_majors.append(major)
    return cleaned_majors


def get_majors(student) -> list:
    majors = {}
    premajors = {}
    colleges = set()

    raw_majors = validate_majors(
        student.majors + student.pending_majors or
        get_requested_majors(student)
    )
    for major in raw_majors:
        if not is_excluded_major(major):
            if is_pre_major(major):
                premajors[major.major_full_name] = major
            else:
                majors[major.major_full_name] = major
                colleges.add(major.college)

    majors_list = list(majors.values())
    premajors_list = list(premajors.values())
    # add each pre-major to the list of majors if its college is not already in
    # the list of colleges
    for premajor in premajors_list:
        if premajor.college not in colleges:
            majors_list.append(premajor)

    majors_list.sort(key=lambda m: m.college, reverse=True)
    return majors_list


def get_major_names(majors):
    if not is_no_sync_college(majors):
        return ';'.join([m.major_full_name for m in majors])
    return ''


def get_primary_major_name(majors):
    if len(majors) and not is_no_sync_college(majors):
        return majors[0].major_full_name


def get_synced_college_name(majors, campus='0'):
    college_code = get_synced_college_code(
        [get_college_for_major(major) for major in majors]
    )
    if college_code is None and campus == '1':
        college_code = 'V'
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
