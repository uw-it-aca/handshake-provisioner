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

FILENAME_TEST_PREFIX = os.getenv('FILENAME_TEST_PREFIX', '')

AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', '')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
AWS_LOCATION = os.getenv('AWS_LOCATION', '')

AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', 'localdev')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', 'localhost')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', 'uw-person')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '5432')

HANDSHAKE_IMPORT_ADMIN_GROUP = 'u_acadev_handshake_admins'

# Settings that control student data provisioning
ENROLLED_STATUS = '12'
ENROLLED_CLASS_CODES = ['1', '2', '3', '4', '5', '8']

APPLICANT_STATUS = '16'
APPLICANT_TYPES = {'FRESHMAN': '1', '2YR TRANSFER': '2', '4YR TRANSFER': '4'}
APPLICANT_CLASS_CODES = ['1', '2', '3', '4', '5', '6', '8']
ATHLETE_CODES = {'25', '26', '27', '30', '31', '32', '33', '34', '40', '41', '42'}
VETERAN_CODES = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '33', '40', '41', '42', '43'}

INCLUDE_CAMPUS_CODES = ['0', '1']
EXCLUDE_COLLEGE_CODES = ['V', 'Z']
EXCLUDE_MAJOR_CODES = ['GEMBA', 'N MATR']
PRE_MAJOR_CODES = ['EPRMJ', 'PSOCS', 'P SW', 'TPRMAJ']

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
    'primary_education:education_level_name',
    'gender',
    'ethnicity',
    'athlete',
    'veteran',
]

MAJOR_COLLEGE_OVERRIDES = {
    'BIOEN': 'J', 'BSE': 'J', 'DATA': 'J', 'PHARBX': 'J', 'PREBSE': 'J',
    'TECH I': 'J',
    'C SCI': 'J2', 'CMP E': 'J2', 'CSE': 'J2', 'CSE E': 'J2', 'CSE M': 'J2',
    'ATM S': 'D', 'ESS': 'D',
    'NUTR S': 'M', 'NUTR': 'M',
    'EEP': 'A',
}

MAJOR_NAME_OVERRIDES = {
    'BA-00': 'Business Administration (General)',
    'ACCTG-01': 'Business Administration (Accounting) - UW Seattle',
    'ACCTG-11': 'Business Administration (Accounting for Business Professionals)',
    'FINANC-01': 'Business Administration (Finance)',
    'MKTG-01': 'Business Administration (Marketing)',
    'ENTRE-01': 'Business Administration (Entrepreneurship)',
    'HRMGT-01': 'Business Administration (Human Resources Management)',
    'I S-01': 'Business Administration (Information Systems)',
    'OSCM-01': 'Business Administration (Operations & Supply Chain Management)',
    'CISB-00': 'Business Administration (Certificate in International Business)',
    'XBSAD-00': 'Business Administration (Exchange)',
    'ACCTGX-01': 'Master of Professional Accounting',
    'MST-00': 'Master of Science in Taxation',
    'I S X-00': 'Master of Science in Information Systems',
    'SCM-00': 'Master of Supply Chain Management',
    'MSBA-00': 'Master of Science in Business Analytics',
    'ENTRE-10': 'Master of Science in Entrepreneurship',
}

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

CLASS_CODE_NAMES = {
    '1': 'Freshman',
    '2': 'Sophomore',
    '3': 'Junior',
    '4': 'Senior',
    '5': 'Senior',
    '8': 'Masters',
}

EMAIL_DOMAIN = 'uw.edu'

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
                "sis_provisioner.context_processors.auth_user",
                "sis_provisioner.context_processors.google_analytics",
                "sis_provisioner.context_processors.django_debug",
            ],
        },
    }
]

LOGGING['loggers']['']['level'] = 'DEBUG'

if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "sis_provisioner", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")
