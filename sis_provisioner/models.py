# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.timezone import get_default_timezone
from sis_provisioner.exceptions import EmptyQueryException
from sis_provisioner.dao.file import read_file, write_file, delete_file
from sis_provisioner.dao.handshake import write_file as write_handshake
from sis_provisioner.dao.student import (
    get_students_for_handshake, get_active_students)
from sis_provisioner.dao.term import (
    current_term, next_term, get_term_by_year_and_quarter)
from sis_provisioner.utils import (
    get_majors, get_major_names, get_primary_major_name, get_college_names,
    is_athlete, is_veteran, get_class_desc, get_education_level_name,
    format_student_number, format_name)
from datetime import datetime, timezone
from logging import getLogger
import csv
import io
import os

logger = getLogger(__name__)

TRUE = 'True'
FALSE = 'False'


class TermManager(models.Manager):
    def current(self):
        academic_term = current_term()
        quarter_int = academic_term.int_key() % 10

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=quarter_int)
        return term

    def next(self):
        academic_term = next_term()
        quarter_int = academic_term.int_key() % 10

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=quarter_int)
        return term


class Term(models.Model):
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4

    QUARTER_CHOICES = (
        (WINTER, 'WIN'), (SPRING, 'SPR'), (SUMMER, 'SUM'), (AUTUMN, 'AUT')
    )

    SWS_LABELS = {
        WINTER: 'winter', SPRING: 'spring', SUMMER: 'summer', AUTUMN: 'autumn'}

    year = models.SmallIntegerField()
    quarter = models.SmallIntegerField(choices=QUARTER_CHOICES)

    objects = TermManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'quarter'],
                                    name='unique_term')
        ]

    @property
    def name(self):
        return '{}{}'.format(
            dict(self.QUARTER_CHOICES).get(self.quarter), self.year)

    def json_data(self):
        return {
            'id': self.pk,
            'year': self.year,
            'quarter': dict(self.QUARTER_CHOICES).get(self.quarter),
        }

    def next(self):
        sws_term = get_term_by_year_and_quarter(
            self.year, self.SWS_LABELS.get(self.quarter))
        nexterm = next_term(sws_term)

        quarter_int = nexterm.int_key() % 10
        term, _ = Term.objects.get_or_create(
            year=nexterm.year, quarter=quarter_int)
        return term


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    created_by = models.CharField(max_length=32, default='automatic')
    created_date = models.DateTimeField()
    generated_date = models.DateTimeField(null=True)
    import_progress = models.SmallIntegerField(default=0)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.CharField(max_length=128, null=True)
    process_id = models.CharField(max_length=64, null=True)

    class Meta:
        abstract = True

    @property
    def filename(self):
        return os.path.basename(self.path or '')

    @property
    def content(self):
        if self.generated_date is not None:
            return read_file(self.path)

    def build(self):
        self.process_id = os.getpid()
        self.save()
        try:
            write_file(self.path, self._generate_csv())
            self.generated_date = datetime.now(timezone.utc)
            logger.info(f'CSV generated for file ID {self.pk}')
        except EmptyQueryException as ex:
            logger.info(f'CSV skipped for file ID {self.pk}: No students')
        except Exception as ex:
            logger.exception(f'CSV failed for file ID {self.pk}: {ex}')

        self.process_id = None
        self.save()

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = datetime.now(timezone.utc)
        if self.path is None:
            self.path = self._create_path()
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        if self.generated_date is not None:
            delete_file(self.path)
        super().delete(**kwargs)

    def json_data(self):
        return {
            'id': self.pk,
            'name': self.filename,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat() if (
                self.created_date is not None) else None,
            'generated_date': self.generated_date.isoformat() if (
                self.generated_date is not None) else None,
            'import_progress': self.import_progress,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'process_id': self.process_id,
        }

    def sisimport(self):
        raise NotImplemented()

    def _create_path(self):
        raise NotImplemented()

    def _generate_csv(self):
        raise NotImplemented()


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
            write_handshake(self.filename, self.content)
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


class ActiveStudentsFileManager(models.Manager):
    def build_file(self):
        import_file = super().get_queryset().filter(
            generated_date__isnull=True, process_id__isnull=True
        ).order_by('created_date').first()

        if import_file is not None:
            import_file.build()
            return import_file


class ActiveStudentsFile(ImportFile):
    '''
    A file containing all active students, currently used for provisioning
    uwnetid and uwregid to LinkedIn Learning.
    '''
    objects = ActiveStudentsFileManager()

    def _create_path(self):
        local_tz = get_default_timezone()
        return self.created_date.replace(tzinfo=timezone.utc).astimezone(
            local_tz).strftime('%Y/%m/active-students-%Y%m%d-%H%M%S.csv')

    def _generate_csv(self):
        s = io.StringIO()
        csv.register_dialect('unix_newline', lineterminator='\n')
        writer = csv.writer(s, dialect='unix_newline')

        writer.writerow([
            'email', 'uwregid', 'prior_uwnetids', 'prior_uwregids'])

        for person in get_active_students():
            writer.writerow([
                f'{person.uwnetid}@{settings.EMAIL_DOMAIN}',
                person.uwregid,
                ';'.join(person.prior_uwnetids),
                ';'.join(person.prior_uwregids),
            ])

        return s.getvalue()
