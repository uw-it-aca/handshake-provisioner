# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from sis_provisioner.exceptions import EmptyQueryException
from sis_provisioner.dao.file import read_file, write_file, delete_file
from datetime import datetime, timezone
from logging import getLogger
import os

logger = getLogger(__name__)


class ImportFile(models.Model):
    path = models.CharField(max_length=128, null=True)
    created_by = models.CharField(max_length=32, default='automatic')
    created_date = models.DateTimeField()
    generated_date = models.DateTimeField(null=True)
    import_progress = models.SmallIntegerField(default=0)
    imported_date = models.DateTimeField(null=True)
    imported_status = models.CharField(max_length=128, null=True)
    process_id = models.CharField(max_length=64, null=True)

    class Meta:
        abstract = True

    @property
    def filename(self):
        return os.path.basename(self.path or '')

    @property
    def content(self):
        if self.generated_date is not None:
            return read_file(self.path)

    def build(self):
        self.process_id = os.getpid()
        self.save()
        try:
            write_file(self.path, self._generate_csv())
            self.generated_date = datetime.now(timezone.utc)
            logger.info(f'CSV generated for file ID {self.pk}')
        except EmptyQueryException as ex:
            logger.info(f'CSV skipped for file ID {self.pk}: No students')
        except Exception as ex:
            logger.exception(f'CSV failed for file ID {self.pk}: {ex}')

        self.process_id = None
        self.save()

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = datetime.now(timezone.utc)
        if self.path is None:
            self.path = self._create_path()
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        if self.generated_date is not None:
            delete_file(self.path)
        super().delete(**kwargs)

    def json_data(self):
        return {
            'id': self.pk,
            'name': self.filename,
            'created_by': self.created_by,
            'created_date': self.created_date.isoformat() if (
                self.created_date is not None) else None,
            'generated_date': self.generated_date.isoformat() if (
                self.generated_date is not None) else None,
            'import_progress': self.import_progress,
            'imported_date': self.imported_date.isoformat() if (
                self.imported_date is not None) else None,
            'imported_status': self.imported_status,
            'process_id': self.process_id,
        }

    def sisimport(self):
        raise NotImplemented()

    def _create_path(self):
        raise NotImplemented()

    def _generate_csv(self):
        raise NotImplemented()
