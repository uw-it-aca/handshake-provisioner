from uw_person_client import UWPersonClient


class UWHandshakeClient(UWPersonClient):

    """
    only campus 0 and 1, enrollment status 12 (16 too?), class codes 1,2,3,4,5, and 8, major codes not 0-EMBA, 0-GEMBA
    don't sync majors for campus 1, college code E (Bothell or Foster)
    """

    def get_students_for_handshake(self):
        students = self.get_registered_students(
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
            if person.student.class_code not in ['1', '2', '3', '4', '5', '8']: continue
            if person.student.campus_code not in ['0', '1']: continue

            foster_mba_program = False
            for major in person.student.majors:
                if major.major_abbr_code in ['0-EMBA', '0-GEMBA']:
                    foster_mba_program = True
                    break
            if foster_mba_program: continue

            majors = []
            for major in person.student.majors:
                if major in ['0-BIOEN', '0-BSE', '0-DATA', '0-PHARBX', '0-PREBSE', '0-TECH I']:
                    major.college = 'J'
                elif major in ['0-C SCI', '0-CMP E', '0-CSE']:
                    major.college = 'J' # code for 'College of Computer Science & Engineering' is just the College of Engineering?
                majors.append(major.college)
            synced_major = max(college for college in majors)
            if synced_major == 'E':
                person.student.majors = []

            if person.student.campus_code == '1':
                person.student.majors = []
            
            handshake_students.append(person)
        
        return handshake_students
