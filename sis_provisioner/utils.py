# Copyright 2024 UW-IT, University of Washington
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


def is_athlete(student):
    return student.special_program_code in getattr(settings, 'ATHLETE_CODES', {})  # noqa


def is_veteran(student):
    return student.veteran_benefit_code in getattr(settings, 'VETERAN_CODES', {})  # noqa


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

    return getattr(settings, 'CLASS_CODE_NAMES', {}).get(class_code)


def get_education_level_name(student):
    if student.class_code in getattr(settings, 'CLASS_CODE_NAMES', {}):
        return 'Masters' if student.class_code == 8 else 'Bachelors'


def format_student_number(number):
    return number.zfill(STUDENT_NUM_LEN)


def get_college_for_major(major):
    return getattr(settings, 'MAJOR_COLLEGE_OVERRIDES', {}).get(
        major.major_abbr_code, major.college)


def is_excluded_college(college_code):
    return college_code in getattr(settings, 'EXCLUDE_COLLEGE_CODES', [])


def get_requested_majors(student):
    requested_codes = [
        student.requested_major1_code,
        student.requested_major2_code,
        student.requested_major3_code
    ]
    if len(requested_codes) == 0:
        return []
    return get_majors_by_code(requested_codes)


def is_pre_major(major):
    return (
        'PRE' in major.major_abbr_code or
        'Undeclared' in major.major_full_name or
        major.major_abbr_code in getattr(settings, 'PRE_MAJOR_CODES', []))


def is_excluded_major(major):
    return major.major_abbr_code in getattr(settings, 'EXCLUDE_MAJOR_CODES')


def validate_majors(majors) -> list:
    cleaned_majors = []
    for major in majors:
        if major.major_full_name and major.college:
            cleaned_majors.append(major)
    return cleaned_majors


def get_major_name(major):
    override_key = '-'.join([
        major.major_abbr_code, str(major.major_pathway or 0).zfill(2)])
    return getattr(settings, 'MAJOR_NAME_OVERRIDES', {}).get(
        override_key, major.major_full_name)


def get_majors(student):
    majors = {}
    premajors = {}
    colleges = set()

    raw_majors = (validate_majors(student.majors) +
                  validate_majors(student.pending_majors))

    if not len(raw_majors):
        logger.debug('No majors found for student {}'.format(
            student.student_number))
        return []

    for major in raw_majors:
        if not is_excluded_major(major):
            if is_pre_major(major):
                premajors[get_major_name(major)] = major
            else:
                majors[get_major_name(major)] = major
                colleges.add(major.college)

    majors_list = list(majors.values())
    premajors_list = list(premajors.values())
    # add each pre-major to the list of majors, if its college is not
    # already in the list of colleges
    for premajor in premajors_list:
        if premajor.college not in colleges:
            majors_list.append(premajor)

    return majors_list


def get_major_names(majors):
    major_names = []
    for major in majors:
        if not is_excluded_college(get_college_for_major(majors[0])):
            major_names.append(get_major_name(major))
    return ';'.join(major_names) if len(major_names) else ''


def get_primary_major_name(majors):
    if (len(majors) and
            not is_excluded_college(get_college_for_major(majors[0]))):
        return get_major_name(majors[0])
    return ''


def get_college_names(majors, campus=0):
    college_names = []
    college_dict = getattr(settings, 'COLLEGES', {})

    for major in majors:
        college_code = get_college_for_major(major)
        if not is_excluded_college(college_code):
            college_name = college_dict.get(college_code)
            if college_name not in college_names:
                college_names.append(college_name)

    if not len(college_names) and campus == 1:
        college_names.append(college_dict.get('V'))

    return ';'.join(college_names) if len(college_names) else ''


def get_ethnicity(student):
    if student.hispanic_under_rep:
        return student.hispanic_group_desc, student.hispanic_long_desc, True
    elif student.ethnic_under_rep:
        return student.ethnic_group_desc, student.ethnic_long_desc, True
    elif student.hispanic_code:
        return student.hispanic_group_desc, student.hispanic_long_desc, False
    elif student.ethnic_code:
        return student.ethnic_group_desc, student.ethnic_long_desc, False
    else:
        return '', '', False


def format_name(first_name, surname):
    try:
        full_name = ' '.join([first_name, surname])
    except TypeError:
        full_name = first_name or surname or ''

    hname = HumanName(full_name)
    hname.capitalize(force=True)
    last = re.sub('^[a-z]', lambda x: x.group().upper(), hname.last)
    return hname.first, hname.middle, (last + ' ' + hname.suffix).strip()
