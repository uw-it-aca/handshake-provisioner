# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import ImportFile


class Command(BaseCommand):
    help = 'Import a file to Handshake'

    def handle(self, *args, **options):
        ImportFile.objects.import_file()
