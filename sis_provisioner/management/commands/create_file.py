# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import HandshakeStudentsFile, Term


class Command(BaseCommand):
    help = 'Creates a TEST Handshake import file for an academic term'

    def add_arguments(self, parser):
        parser.add_argument(
            'term', type=str, default='next', choices=['current', 'next'],
            help='Create file for term <term>')

    def handle(self, *args, **options):
        term_str = options.get('term')

        if term_str == 'next':
            term = Term.objects.next()
        else:
            term = Term.objects.current()

        import_file = HandshakeStudentsFile.objects.add_file(
            term=term, is_test_file=True)
        import_file.build()
