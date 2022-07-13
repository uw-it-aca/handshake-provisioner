from django.conf import settings
from uw_person_client import UWPersonClient


class UWHandshakeClient:

    """
    only campus 0 and 1, enrollment status 12 (16 too?), class codes 1,2,3,4,5, and 8, major codes not 0-EMBA, 0-GEMBA
    don't sync majors for campus 1, college code E (Bothell or Foster)
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

    def _update_college_for_majors(self, majors):
        engr_majors = getattr(settings, 'ENGR_COLLEGE_MAJORS', [])
        for major in majors:
            if major.major_abbr_code in engr_majors:
                major.college = 'J'

    def get_students_for_handshake(self):
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
