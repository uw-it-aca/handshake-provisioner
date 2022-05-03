# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from storages.backends.s3boto import S3BotoStorage


class HandshakeStorage():
    @property
    def storage(self):
        if not hasattr(self, '_storage'):
            self._storage = S3BotoStorage(
                'bucket_name': getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                'default_acl': None
            )
        return self._storage

    def read_file(self.path):
        if not self.storage.exists(path):
            raise ObjectDoesNotExist()

        with self.storage.open(path, mode='r') as f:
            content = f.read()

        return content

    def write_file(self, path, data):
        with self.storage.open(path, mode='wb') as f:
            f.write(data)
