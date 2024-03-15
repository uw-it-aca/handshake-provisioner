from .base_settings import *
from google.oauth2 import service_account
import os

INSTALLED_APPS += [
    'sis_provisioner.apps.SISProvisionerConfig',
]

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
    MEDIA_ROOT = os.getenv('MEDIA_ROOT', '/app/data')
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'sis_provisioner.cache.RestClientsCache'
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
            'OPTIONS': {
                'project_id': os.getenv('STORAGE_PROJECT_ID', ''),
                'bucket_name': os.getenv('STORAGE_BUCKET_NAME', ''),
                'location': os.path.join(os.getenv('STORAGE_DATA_ROOT', '')),
                'credentials': service_account.Credentials.from_service_account_file(
                    '/gcs/credentials.json'),
            }
        },
        'handshake': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'region_name': os.getenv('AWS_S3_REGION_NAME', ''),
                'bucket_name': os.getenv('AWS_STORAGE_BUCKET_NAME', ''),
                'location': os.getenv('AWS_LOCATION', ''),
                'access_key': os.getenv('AWS_ACCESS_KEY_ID', ''),
                'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
            }
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
    CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('CLUSTER_CNAME')]

FILENAME_TEST_PREFIX = os.getenv('FILENAME_TEST_PREFIX', '')

AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', 'localdev')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', 'localhost')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', 'uw-person')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '5432')

RESTCLIENTS_SWS_OAUTH_BEARER = os.getenv('RESTCLIENTS_SWS_OAUTH_BEARER', '')

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
EXCLUDE_COLLEGE_CODES = ['Z']
EXCLUDE_MAJOR_CODES = ['N MATR']
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
    'primary_education:college_names',
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

LABEL_CSV_HEADER = [
    'identifier',
    'identifiable_type',
    'user_type',
    'sp_pgm_descrip',
    's1_visa_type',
    'DRS',
    'athlete',
    'veteran',
]

MAJOR_COLLEGE_OVERRIDES = {
    'BIOEN': 'J', 'BSE': 'J', 'DATA': 'J', 'PHARBX': 'J', 'PREBSE': 'J',
    'C SCI': 'J2', 'CMP E': 'J2', 'CSE': 'J2', 'CSE E': 'J2', 'CSE M': 'J2',
    'ATM S': 'D', 'ESS': 'D', 'NUTR S': 'M', 'NUTR': 'M', 'EEP': 'A',
    'MUSEOX': 'S', 'TECH I': 'J',
}

MAJOR_NAME_OVERRIDES = {
    'B A-00': 'Business Administration (General)',
    'BA-00': 'Business Administration (General)',
    'ACCTG-00': 'Business Administration (Accounting) - UW Seattle',
    'ACCTG-01': 'Business Administration (Accounting) - UW Seattle',
    'ACCTG-11': 'Business Administration (Accounting for Business Professionals)',
    'FINANC-00': 'Business Administration (Finance)',
    'FINANC-01': 'Business Administration (Finance)',
    'MKTG-01': 'Business Administration (Marketing)',
    'MKTG-10': 'Business Administration (Marketing)',
    'ENTRE-00': 'Business Administration (Entrepreneurship)',
    'ENTRE-01': 'Business Administration (Entrepreneurship)',
    'HRMGT-01': 'Business Administration (Human Resources Management)',
    'I S-00': 'Business Administration (Information Systems)',
    'I S-01': 'Business Administration (Information Systems)',
    'OSCM-00': 'Business Administration (Operations & Supply Chain Management)',
    'OSCM-01': 'Business Administration (Operations & Supply Chain Management)',
    'CISB-00': 'Business Administration (Certificate in International Business)',
    'XBSAD-00': 'Business Administration (Exchange)',
    'ACCTGX-01': 'Master of Professional Accounting',
    'MST-00': 'Master of Science in Taxation',
    'I S X-00': 'Master of Science in Information Systems',
    'SCM-00': 'Master of Supply Chain Management',
    'MSBA-00': 'Master of Science in Business Analytics',
    'ENTRE-10': 'Master of Science in Entrepreneurship',
    'EMBA-00': 'Master of Business Administration (Executive)',
    'GEMBA-00': 'Master of Business Administration (Global Executive)',
    'MBA EX-00': 'Master of Business Administration (Evening)',
    'MBA-00': 'Master of Business Administration (Full-Time)',
    'MBA-20': 'Master of Business Administration (Hybrid)',
    'TMMBA-00': 'Master of Business Administration (Technology Management)',
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
    'K': 'College of the Environment',
    'L': 'College of the Environment',
    'M': 'School of Public Health',
    'N': 'School of Nursing',
    'O': 'Interschool or Intercollege Programs',
    'P': 'School of Pharmacy',
    'Q': 'Evans School of Public Policy & Governance',
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

if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "sis_provisioner", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")
