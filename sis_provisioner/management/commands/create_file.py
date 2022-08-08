# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import ImportFile
from sis_provisioner.utils import DateToTerm


class Command(BaseCommand):
    help = 'Creates the Handshake import file for an academic term'

    def add_arguments(self, parser):
        parser.add_argument(
            'term', type=str, default='next', choices=['current', 'next'],
            help='Create file for term <term>')

    def handle(self, *args, **options):
        term_str = options.get('term')

        academic_term = DateToTerm().current_term() if (
            term_str == 'current') else DateToTerm().next_term()

        import_file = ImportFile()
        import_file.create(academic_term)
