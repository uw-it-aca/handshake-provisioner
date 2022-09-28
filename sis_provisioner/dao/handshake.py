# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from storages.backends.s3boto3 import S3Boto3Storage


def read_file(path):
    storage = S3Boto3Storage()
    if not storage.exists(path):
        raise ObjectDoesNotExist()

    with storage.open(path, mode='r') as f:
        content = f.read()

    return content


def write_file(path, data):
    storage = S3Boto3Storage()
    with storage.open(path, mode='wb') as f:
        f.write(data)
