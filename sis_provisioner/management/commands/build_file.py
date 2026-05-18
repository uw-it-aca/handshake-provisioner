# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models.handshake import (
    HandshakeStudentsFile, HandshakeLabelsFile, ActiveStudentsFile)
from sis_provisioner.models.uconnect import UconnectStudentsFile


class Command(BaseCommand):
    help = 'Build the csv data for an import file.'

    def handle(self, *args, **options):
        (HandshakeStudentsFile.objects.build_file() or
            UconnectStudentsFile.objects.build_file() or
            HandshakeLabelsFile.objects.build_file() or
            ActiveStudentsFile.objects.build_file())
