# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import storages


def read_file(path):
    storage = storages['handshake']
    if not storage.exists(path):
        raise ObjectDoesNotExist()

    with storage.open(path, mode='r') as f:
        content = f.read()

    return content


def write_file(path, data):
    storage = storages['handshake']
    with storage.open(path, mode='wb') as f:
        f.write(data)
