# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from uw_sws.util import fdao_sws_override
from sis_provisioner.dao.term import current_term, next_term


@fdao_sws_override
class AcademicTermTest(TestCase):
    def test_current_term(self):
        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-10-15 00:00:00'):
            term = current_term()
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, 'autumn')

    def test_next_term(self):
        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-01-15 00:00:00'):
            term = next_term()
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, 'spring')

        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-1-1 00:00:00'):
            term = next_term()
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, 'winter')
