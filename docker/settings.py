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

FILENAME_PREFIX = os.getenv('FILENAME_PREFIX', '')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')

AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', 'localdev')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', 'localhost')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', 'uw-person')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '5432')

# Settings that control student data provisioning
ENROLL_STATUS = '12'
INCLUDE_CLASS_CODES = ['1', '2', '3', '4', '5', '8']
INCLUDE_CAMPUS_CODES = ['0', '1']
EXCLUDE_MAJOR_CODES = ['0-GEMBA']
ENGR_COLLEGE_MAJORS = ['0-BIOEN', '0-BSE', '0-DATA', '0-PHARBX', '0-PREBSE',
                        '0-TECH I']
CSE_COLLEGE_MAJORS = ['0-C SCI', '0-CMP E', '0-CSE']

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
    'A': 'Interdisciplinary Undergraduate Programs',
    'B': 'College of Built Environments',
    'C': 'College of Arts & Sciences',
    'D': 'College of the Environment',
    'E': 'Foster School of Business',
    'H': 'College of Education',
    'J': 'College of Engineering',
    'J2': 'School of Computer Science & Engineering',
    'K': 'College of Ocean & Fishery Sciences',
    'L': 'College of Forest Resources',
    'M': 'School of Public Health',
    'N': 'School of Nursing',
    'O': 'Interschool or Intercollege Programs',
    'P': 'School of Pharmacy',
    'Q': 'Evans School of Public Affairs',
    'R': 'Interdisciplinary Graduate Programs',
    'S': 'The Information School',
    'T': 'School of Social Work',
    'U': 'School of Dentistry',
    'V': 'UW Bothell',
    'X': 'School of Law',
    'Y': 'School of Medicine',
}

CLASS_CODES = {
    '1': 'Freshman',
    '2': 'Sophomore',
    '3': 'Junior',
    '4': 'Senior',
    '5': 'Senior',
    '8': 'Masters',
}

EMAIL_DOMAIN = 'uw.edu'
