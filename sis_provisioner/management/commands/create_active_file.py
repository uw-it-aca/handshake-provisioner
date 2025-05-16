# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import ActiveStudentsFile


class Command(BaseCommand):
    help = 'Creates an active student import file'

    def handle(self, *args, **options):
        ActiveStudentsFile().save()
