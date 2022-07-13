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
INCLUDED_CLASS_CODES = ["1", "2", "3", "4", "5", "8"]
INCLUDED_CAMPUS_CODES = ["0", "1"]
EXCLUDED_MAJOR_CODES = ["0-EMBA", "0-GEMBA"]
ENGR_COLLEGE_MAJORS = ["0-BIOEN", "0-BSE", "0-DATA", "0-PHARBX", "0-PREBSE",
                        "0-TECH I", "0-C SCI", "0-CMP E", "0-CSE"]
