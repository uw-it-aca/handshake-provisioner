# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist


def read_file(path):
    if not default_storage.exists(path):
        raise ObjectDoesNotExist()

    with default_storage.open(path, mode='r') as f:
        content = f.read()

    return content


def write_file(path, data):
    with default_storage.open(path, mode='wb') as f:
        f.write(data)


def delete_file(path):
    if not default_storage.exists(path):
        raise ObjectDoesNotExist()

    default_storage.delete(path)
