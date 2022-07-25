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

COLLEGES = {
    'A': 'Undergraduate Interdisciplinary Programs',
    'B': 'College of Built Environment',
    'C': 'College of Arts & Sciences',
    'D': 'College of the Environment',
    'E': 'School of Business',
    'H': 'College of Education',
    'J': 'College of Engineering',
    'M': 'School of Public Health & Community Med',
    'N': 'School of Nursing',
    'O': 'Interschool or Intercollege Programs',
    'P': 'School of Pharmacy',
    'Q': 'School of Public Affairs',
    'R': 'Interdisciplinary Graduate Programs',
    'S': 'The Information School',
    'T': 'School of Social Work',
    'U': 'School of Dentistry',
    'V': 'University of Washington, Bothell',
    'X': 'School of Law',
    'Y': 'School of Medicine',
    'Z': 'University of Washington, Tacoma',
}
