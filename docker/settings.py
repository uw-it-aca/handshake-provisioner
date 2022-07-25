from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'sis_provisioner.apps.SISProvisionerConfig',
]

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/data')
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_PROJECT_ID = os.getenv('STORAGE_PROJECT_ID', '')
    GS_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME', '')
    GS_LOCATION = os.path.join(os.getenv('STORAGE_DATA_ROOT', ''))
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        '/gcs/credentials.json')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')

# Settings that control student data provisioning
ENROLL_STATUS = '12'
INCLUDE_CLASS_CODES = ['1', '2', '3', '4', '5', '8']
INCLUDE_CAMPUS_CODES = ['0', '1']
EXCLUDE_MAJOR_CODES = ['0-EMBA', '0-GEMBA']
ENGR_COLLEGE_MAJORS = ['0-BIOEN', '0-BSE', '0-DATA', '0-PHARBX', '0-PREBSE',
                        '0-TECH I', '0-C SCI', '0-CMP E', '0-CSE']

HANDSHAKE_CSV_HEADER = [
    'username',
    'auth_identifier',
    'card_id',
    'school_year_name',
    'last_name',
    'first_name',
    'middle_name',
    'preferred_name',
    'primary_education:college_name',
    'email_address',
    'campus_name',
    'primary_education:major_names',
    'primary_education:primary_major_name',
    'primary_education:currently_attending',
]

NEW_CSV_HEADERS = [
    'gender',
    'ethnicity',
    'athlete',
    'veteran',
    'work_study_eligible',
    'primary_education:education_level_name',
]

ATHLETE_CODES = [
    '25', '26', '27', '30', '31', '32', '33', '34', '40', '41', '42'
]

COLLEGES = {
    'A': 'UNDERGRADUATE INTERDISCIPLINARY PROGRAMS',
    'B': 'COLLEGE OF BUILT ENVIRONMENT',
    'C': 'COLLEGE OF ARTS AND SCIENCES',
    'D': 'COLLEGE OF THE ENVIRONMENT',
    'E': 'SCHOOL OF BUSINESS',
    'H': 'COLLEGE OF EDUCATION',
    'J': 'COLLEGE OF ENGINEERING',
    'M': 'SCHOOL OF PUBLIC HEALTH & COMMUNITY MED',
    'N': 'SCHOOL OF NURSING',
    'O': 'INTERSCHOOL OR INTERCOLLEGE PROGRAMS',
    'P': 'SCHOOL OF PHARMACY',
    'Q': 'SCHOOL OF PUBLIC AFFAIRS',
    'R': 'INTERDISCIPLINARY GRADUATE PROGRAMS',
    'S': 'THE INFORMATION SCHOOL',
    'T': 'SCHOOL OF SOCIAL WORK',
    'U': 'SCHOOL OF DENTISTRY',
    'V': 'UNIVERSITY OF WASHINGTON, BOTHELL',
    'X': 'SCHOOL OF LAW',
    'Y': 'SCHOOL OF MEDICINE',
    'Z': 'UNIVERSITY OF WASHINGTON, TACOMA',
}
