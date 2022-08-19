# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from sis_provisioner.models import AcademicTerm
from datetime import datetime


class AcademicTermTest(TestCase):
    def test_name(self):
        term = AcademicTerm(date=datetime(2020, 1, 10))
        self.assertEqual(term.name, 'WIN2020')
        self.assertEqual(term.next().name, 'SPR2020')
        self.assertEqual(term.next().name, 'SUM2020')
        self.assertEqual(term.next().name, 'AUT2020')

    def test_term_from_current_datetime(self):
        term = AcademicTerm()
        self.assertEqual(term.year, datetime.now().year)
        self.assertEqual(term.current(),
                         AcademicTerm(date=datetime.now()).current())

    def test_term_from_datetime(self):
        term = AcademicTerm(date=datetime(2020, 1, 1))
        self.assertEqual(term.year, 2020)
        self.assertEqual(term.quarter, 4)

        term.next()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 1)

        term.previous()
        self.assertEqual(term.year, 2020)
        self.assertEqual(term.quarter, 4)

        term = AcademicTerm(date=datetime(2022, 4, 1))
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 2)

        term.next()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 3)

        term.previous()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 2)

        term = AcademicTerm(date=datetime(2021, 6, 20))
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 2)

        term.next()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 3)

        term.previous()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 2)

        term = AcademicTerm(date=datetime(2021, 6, 21))
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 3)

        term.next()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 4)

        term.previous()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 3)

        term = AcademicTerm(date=datetime(2021, 10, 1))
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 4)

        term.next()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 1)

        term.previous()
        self.assertEqual(term.year, 2021)
        self.assertEqual(term.quarter, 4)

        term = AcademicTerm(date=datetime(2022, 3, 27))
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 1)

        term.next()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 2)

        term.previous()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 1)

        term = AcademicTerm(date=datetime(2022, 3, 28))
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 2)

        term.next()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 3)

        term.previous()
        self.assertEqual(term.year, 2022)
        self.assertEqual(term.quarter, 2)
