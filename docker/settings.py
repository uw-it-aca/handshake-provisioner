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

AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', '')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
AWS_LOCATION = os.getenv('AWS_LOCATION', '')

AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', 'localdev')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', 'localhost')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', 'uw-person')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '5432')

# Settings that control student data provisioning
ENROLL_STATUS = '12'
INCLUDE_CLASS_CODES = ['1', '2', '3', '4', '5', '8']
INCLUDE_CAMPUS_CODES = ['0', '1', '0.0', '1.0']
EXCLUDE_MAJOR_CODES = ['GEMBA']
ENGR_COLLEGE_MAJORS = ['BIOEN', 'BSE', 'DATA', 'PHARBX', 'PREBSE', 'TECH I']
CSE_COLLEGE_MAJORS = ['C SCI', 'CMP E', 'CSE', 'CSE E', 'CSE M']

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

# If you have file data, define the path here
# DATA_ROOT = os.path.join(BASE_DIR, "app_name/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sis_provisioner.context_processors.google_analytics",
                "sis_provisioner.context_processors.django_debug",
            ],
        },
    }
]


if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "sis_provisioner", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")
