# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import ImportFile


class Command(BaseCommand):
    help = 'Import a file to Handshake'

    def add_arguments(self, parser):
        parser.add_argument('file_id', type=int,
                            help='File ID to import to Handshake')

    def handle(self, *args, **options):
        file_id = options.get('file_id')
        import_file = ImportFile.objects.get(pk=file_id)
        import_file.sisimport()
