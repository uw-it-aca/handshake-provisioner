# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
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


def get_class_desc(student):
    class_code = student.class_code
    majors = student.majors
    if class_code not in getattr(settings, 'INCLUDE_CLASS_CODES', []):
        return None
    if any('MBA' in major.major_abbr_code for major in majors) and \
            get_synced_college_name(majors) == 'Foster School of Business':
        return 'Masters of Business Administration'
    return getattr(settings, 'CLASS_CODES', {}).get(class_code, None)


def format_student_number(number):
    return '0' * (7-len(number)) + number


def get_college_for_major(major):
    if major.major_abbr_code in getattr(settings, 'ENGR_COLLEGE_MAJORS', []):
        return 'J'
    if major.major_abbr_code in getattr(settings, 'CSE_COLLEGE_MAJORS', []):
        return 'J2'
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
    return ';'.join([m.major_full_name for m in majors])


def get_primary_major_name(majors):
    majors = get_majors(majors)
    try:
        return majors[0].major_full_name
    except (IndexError, AttributeError):
        pass


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

class DateToTerm():
    def get_fall_start_date(self, year):
        sept = datetime(year, 9, 24)
        return sept + relativedelta(weekday=2)  # last Wednesday


    def get_winter_start_date(self, year):
        jan = datetime(year, 1, 2)
        # if Jan 1 is Sunday or Monday, start on Jan 3
        if jan.weekday() in [0, 1]:
            return jan.replace(day=3)
        return jan + relativedelta(weekday=0)  # first Monday after Jan 1


    def get_spring_start_date(self, year):
        start = self.get_winter_start_date(year) +\
            relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after winter


    def get_summer_start_date(self, year):
        start = self.get_spring_start_date(year) +\
            relativedelta(weeks=11, days=1)
        return start + relativedelta(weekday=0)  # second Monday after spring


    def get_quarter_from_date(self, dt: datetime):
        terms = [self.get_winter_start_date(dt.year),
                 self.get_spring_start_date(dt.year),
                 self.get_summer_start_date(dt.year),
                 self.get_fall_start_date(dt.year)]
        
        idx = 0
        while idx < len(terms) and dt >= terms[idx]:
            idx += 1
        return idx if idx > 0 else 4


    def term_from_datetime(self, dt: datetime):
        return (dt.year, self.get_quarter_from_date(dt))


    def current_term(self):
        return self.term_from_datetime(datetime.now())


    def next_term(self):
        current = self.current_term()
        if current[1] == 4:
            return (current[0] + 1, 1)
        return (current[0], current[1] + 1)


    def current_next_terms(self):
        return [self.current_term(), self.next_term()]
