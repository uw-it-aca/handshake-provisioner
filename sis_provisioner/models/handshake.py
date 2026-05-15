# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.timezone import get_default_timezone
from sis_provisioner.models.importfile import ImportFile
from sis_provisioner.models.term import Term
from sis_provisioner.dao.handshake import write_file
from sis_provisioner.dao.student import get_students_for_handshake
from sis_provisioner.utils import (
    get_majors, get_major_names, get_primary_major_name, get_college_names,
    is_athlete, is_veteran, get_class_desc, get_education_level_name,
    format_student_number, format_name)
from datetime import datetime, timezone
from logging import getLogger
import csv
import io

logger = getLogger(__name__)

TRUE = 'True'
FALSE = 'False'


class HandshakeStudentsFileManager(models.Manager):
    def build_file(self):
        import_file = super().get_queryset().filter(
            generated_date__isnull=True, process_id__isnull=True
        ).order_by('created_date').first()

        if import_file is None:
            return

        import_file.build()

        # Automatically created files are automatically imported
        if (import_file.generated_date is not None and
                import_file.created_by == 'automatic'):
            import_file.sisimport()

        return import_file


class HandshakeStudentsFile(ImportFile):
    '''
    A file containing enrolled students for a term, used for provisioning
    student attributes to Handshake.
    '''
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_test_file = models.BooleanField(default=False)

    objects = HandshakeStudentsFileManager()

    def sisimport(self):
        if self.generated_date is None:
            raise ObjectDoesNotExist

        try:
            write_file(self.filename, self.content)
            self.imported_status = 200
            self.imported_date = datetime.now(timezone.utc)
            logger.info(f'File ID {self.pk} imported')
        except Exception as ex:
            logger.critical(ex, exc_info=True)
            self.imported_status = 500
            raise
        finally:
            self.save()

    def json_data(self):
        data = super().json_data()
        data['term'] = self.term.json_data()
        data['is_test_file'] = self.is_test_file
        data['api_path'] = reverse('handshake-file', kwargs={
                'file_id': self.pk}),
        return data

    def _create_path(self):
        name = self.term.name
        prefix = getattr(settings, 'FILENAME_TEST_PREFIX')

        if self.is_test_file and prefix is not None and len(prefix):
            name = f'{prefix}-{name}'

        local_tz = get_default_timezone()
        return self.created_date.replace(tzinfo=timezone.utc).astimezone(
            local_tz).strftime(f'%Y/%m/{name}-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.HANDSHAKE_CSV_HEADER)

        blocked_students = BlockedHandshakeStudent.objects.all_usernames()

        for student in get_students_for_handshake(self.term):
            if student.person.uwnetid in blocked_students:
                continue

            majors = get_majors(student)

            first_name, middle_name, last_name = format_name(
                student.person.first_name, student.person.surname)

            writer.writerow([
                student.person.uwnetid,
                student.person.uwnetid,
                format_student_number(student.student_number),
                get_class_desc(student, majors),
                last_name,
                first_name,
                middle_name,
                student.person.preferred_first_name,
                get_college_names(majors, student.campus_code),
                f'{student.person.uwnetid}@{settings.EMAIL_DOMAIN}',
                student.campus_desc,
                get_major_names(majors),
                get_primary_major_name(majors),
                TRUE,  # primary_education:currently_attending
                get_education_level_name(student),
                student.gender,
                student.hispanic_group_desc if (
                    student.hispanic_group_desc is not None) else (
                        student.ethnic_group_desc),
                TRUE if is_athlete(student) else FALSE,
                TRUE if is_veteran(student) else FALSE,
                # 'work_study_eligible',  # Currently unavailble
            ])

        return s.getvalue()


class HandshakeLabelsFileManager(models.Manager):
    def build_file(self):
        import_file = super().get_queryset().filter(
            generated_date__isnull=True, process_id__isnull=True
        ).order_by('created_date').first()

        if import_file is None:
            return

        import_file.build()

        # Automatically created files are automatically imported
        if (import_file.generated_date is not None and
                import_file.created_by == 'automatic'):
            import_file.sisimport()

        return import_file


class HandshakeLabelsFile(ImportFile):
    '''
    A file containing enrolled student labels for a term, used for provisioning
    student labels to Handshake.
    '''
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    is_test_file = models.BooleanField(default=False)

    objects = HandshakeLabelsFileManager()

    def json_data(self):
        data = super().json_data()
        data['term'] = self.term.json_data()
        data['is_test_file'] = self.is_test_file
        # data['api_path'] = reverse('handshake-file', kwargs={
        #         'file_id': self.pk}),
        return data

    def sisimport(self):
        pass

    def _create_path(self):
        name = f'{self.term.name}-LABELS'
        prefix = getattr(settings, 'FILENAME_TEST_PREFIX')

        if self.is_test_file and prefix is not None and len(prefix):
            name = f'{prefix}-{name}'

        local_tz = get_default_timezone()
        return self.created_date.replace(tzinfo=timezone.utc).astimezone(
            local_tz).strftime(f'%Y/%m/{name}-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow(settings.LABEL_CSV_HEADER)

        blocked_students = BlockedHandshakeStudent.objects.all_usernames()

        students = {}
        for student in get_students_for_handshake(self.term):
            uwnetid = student.person.uwnetid
            if uwnetid not in blocked_students:
                students[uwnetid] = self._student_labels(student)

        for uwnetid in students:
            for label in students[uwnetid]:
                writer.writerow([
                    f'{uwnetid}@{settings.EMAIL_DOMAIN}',
                    'User',         # User|Contact|Employer|Job
                    'Students',     # Students|Career Services
                    f'cic-{label}',
                    'normal',       # normal|public
                ])
        return s.getvalue()

    def _student_labels(self, student):
        labels = []
        if student.disability_ind:
            labels.append('drs')
        if (student.special_program_code == '1' or
                student.special_program_code == '2'):
            labels.append('eop 1')
        elif student.special_program_code == '13':
            labels.append('eop 3')
        if student.visa_type == 'F1':
            labels.append('f1 international student')
        elif student.visa_type == 'J1':
            labels.append('j1 international student')
        elif student.visa_type is not None and len(student.visa_type):
            labels.append('non-f1 or j1 international student')
        if is_athlete(student):
            labels.append('student athlete')
        if is_veteran(student):
            labels.append('veteran')
        if student.hispanic_under_rep or student.ethnic_under_rep:
            labels.append('urm')
        return labels


class BlockedHandshakeStudentManager(models.Manager):
    def all_usernames(self):
        usernames = super().get_queryset().all().values_list(
            'username', flat=True)
        return set(usernames)


class BlockedHandshakeStudent(models.Model):
    username = models.CharField(max_length=20, null=False, unique=True)
    added_by = models.CharField(max_length=20)
    added_date = models.DateTimeField()
    reason = models.CharField(max_length=250, null=True)

    objects = BlockedHandshakeStudentManager()

    def json_data(self):
        return {
            'id': self.pk,
            'username': self.username,
            'added_by': self.added_by,
            'added_date': self.added_date.isoformat(),
            'reason': self.reason,
        }
