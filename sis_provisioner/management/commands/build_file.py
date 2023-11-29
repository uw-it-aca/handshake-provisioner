# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import (
    HandshakeStudentsFile, HandshakeLabelsFile, ActiveStudentsFile)


class Command(BaseCommand):
    help = 'Build the csv data for an import file.'

    def handle(self, *args, **options):
        (HandshakeStudentsFile.objects.build_file() or
            HandshakeLabelsFile.objects.build_file() or
            ActiveStudentsFile.objects.build_file())
