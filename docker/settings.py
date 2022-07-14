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
INCLUDED_CLASS_CODES = ['1', '2', '3', '4', '5', '8']
INCLUDED_CAMPUS_CODES = ['0', '1']
EXCLUDED_MAJOR_CODES = ['0-EMBA', '0-GEMBA']
ENGR_COLLEGE_MAJORS = ['0-BIOEN', '0-BSE', '0-DATA', '0-PHARBX', '0-PREBSE',
                        '0-TECH I', '0-C SCI', '0-CMP E', '0-CSE']

"""
maps fields of the expected handshake fields to the fields as they appear in the
student data

adding '[]' after an attribute indicates that it is a list of values, and an
index inside means to only grab that index of the attribute list
"""
HANDSHAKE_FIELDNAMES = {
    'auth_identifier': 'uwnetid',
    'username': 'uwnetid',
    'email_address': 'student:student_email',
    'card_id': 'student:student_number',
    'school_year_name': 'student:class_code',
    'campus_name': 'student:campus_code',
    'last_name': 'last_name',
    'first_name': 'first_name',
    'middle_name': 'preferred_middle_name',
    'preferred_name': 'preferred_first_name',
    'primary_education:college_name': 'student:majors[]:college',
    'primary_education:major_names[]': 'student:majors[]:major_name',
    'primary_education:primary_major_name': 'student:majors[0]:major_name',
    # 'primary_education:education_level_name': '',
    'gender': 'student:gender',
    'ethnicity': 'assigned_ethnic_code',
    # 'athlete': '',
    'veteran': 'student:veteran_benefit_code',
    # 'work_study_eligible': ''
}
