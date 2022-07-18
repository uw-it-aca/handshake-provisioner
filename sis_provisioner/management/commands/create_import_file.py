# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import ImportFile


class Command(BaseCommand):
    help = 'Creates the Handshake import file'

    def handle(self, *args, **options):
        import_file = ImportFile()
        import_file.create()
