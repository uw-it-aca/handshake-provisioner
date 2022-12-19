# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from sis_provisioner.models import HandshakeStudentsFile, Term


class Command(BaseCommand):
    help = 'Creates a TEST Handshake import file for an academic term'

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--test', action='store_true', dest='test', default=False,
            help='Create TEST file')
        parser.add_argument(
            'term', type=str, default='current', choices=['current', 'next'],
            help='Create file for term <term>')

    def handle(self, *args, **options):
        is_test_file = options.get('test')
        term_str = options.get('term')

        if term_str == 'next':
            term = Term.objects.next()
        else:
            term = Term.objects.current()

        HandshakeStudentsFile(term=term, is_test_file=is_test_file).save()
