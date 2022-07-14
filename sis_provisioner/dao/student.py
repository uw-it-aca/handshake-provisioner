from django.conf import settings
from uw_person_client import UWPersonClient
import csv
import re


class UWHandshakeClient:

    """
    only campus 0 and 1, enrollment status 12 (16 too?), class codes 1,2,3,4,5,
    and 8, major codes not 0-EMBA, 0-GEMBA
    """

    def __init__(self):
        self.client = UWPersonClient()

    @staticmethod
    def valid_class_code(class_code):
        class_codes = getattr(settings, 'INCLUDED_CLASS_CODES', [])
        return class_code in class_codes

    @staticmethod
    def valid_campus_code(campus_code):
        campus_codes = getattr(settings, 'INCLUDED_CAMPUS_CODES', [])
        return campus_code in campus_codes

    @staticmethod
    def valid_major_code(major_codes):
        excluded_codes = getattr(settings, 'EXCLUDED_MAJOR_CODES', [])
        for excluded_code in excluded_codes:
            if excluded_code in major_codes:
                return False
        return True

    @staticmethod
    def get_handshake_fieldnames_map() -> dict:
        return getattr(settings, 'HANDSHAKE_FIELDNAMES', {})

    def _update_college_for_majors(self, majors: list):
        engr_majors = getattr(settings, 'ENGR_COLLEGE_MAJORS', [])
        for major in majors:
            if major.major_abbr_code in engr_majors:
                major.college = 'J'

    def _get_synced_major(self, majors: list) -> str:
        # get most alphabetically last college major code
        return max(college for college in majors) if majors else None

    # empty majors list for campus 1 and college E
    def _filter_students(self, students: list):
        for person in students:
            if person['campus_name'] == '1' or self._get_synced_major(
                    person['primary_education:college_name']) == 'E':
                person['primary_education:major_names'] = []
                person['primary_education:primary_major_name'] = None

    def _init_dict(self, fieldnames: list) -> dict:
        new_dict = {}
        for fieldname in fieldnames:
            if '[]' in fieldname:
                new_dict[fieldname.replace('[]', '')] = []
            else:
                new_dict[fieldname] = ''
        return new_dict

    # follow path in current_dict and insert val
    def _fill_dict(self, current_dict, val, path: list):
        for key in path[:-1]:
            if '[]' in key:
                key = key.replace('[]', '')
            current_dict = current_dict[key]
        key = path[-1].replace('[]', '')
        current_dict[key] = val

    def _get_from_dict(self, current_dict, path: list):
        for count, key in enumerate(path[:-1]):
            if '[]' in key:
                key = key.replace('[]', '')
                return [self._get_from_dict(item, path[count+1:]) \
                        for item in current_dict[key]]
            elif re.search('\[\d+\]', key):
                index = re.findall('\[\d+\]', key)[0]
                current_dict = current_dict[key.replace(index, '')]
                if current_dict:
                    current_dict = current_dict[int(re.findall('\d+', index)[0])]
                else:
                    return None
            else:
                current_dict = current_dict[key]
        return current_dict[path[-1]]

    def create_handshake_dicts(self, students: list, fieldnames) -> list:
        handshake_dicts = []
        for student in students:
            handshake_dict = self._init_dict(fieldnames)
            for handshake_key, db_key in self.get_handshake_fieldnames_map().items():
                val = self._get_from_dict(student, db_key.split(':'))
                self._fill_dict(handshake_dict, val, [handshake_key])
            handshake_dicts.append(handshake_dict)
        # filter out campus 1 and college E majors
        self._filter_students(handshake_dicts)
        return handshake_dicts

    def get_students_for_handshake(self) -> list:
        students = self.client.get_registered_students(
            include_employee=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_intended_majors=False,
            include_student_pending_majors=False,
            include_student_requested_majors=False)

        handshake_students = []

        for person in students:
            if not self.valid_class_code(person.student.class_code):
                continue

            if not self.valid_campus_code(person.student.campus_code):
                continue

            if not self.valid_major_code(person.student.majors):
                continue

            self._update_college_for_majors(person.student.majors)

            handshake_students.append(person)

        return handshake_students

    def get_student_csv(self, filename) -> str:
        students = self.get_students_for_handshake()
        students_list = [student.to_dict() for student in students]
        fieldnames = [key.replace('[]', '') for key in self.get_handshake_fieldnames_map().keys()]
        students_dicts = self.create_handshake_dicts(students_list, fieldnames)

        if students_dicts:
            with open(filename, 'w', newline='') as csvfile:
                csv.register_dialect('unix_newline', lineterminator='\n')
                writer = csv.DictWriter(csvfile, fieldnames, dialect='unix_newline')

                writer.writeheader()
                writer.writerows(students_dicts)

            return filename
