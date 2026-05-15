# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.db import models
from sis_provisioner.dao.term import (
    current_term, next_term, get_term_by_year_and_quarter)


class TermManager(models.Manager):
    def current(self):
        academic_term = current_term()
        quarter_int = academic_term.int_key() % 10

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=quarter_int)
        return term

    def next(self):
        academic_term = next_term()
        quarter_int = academic_term.int_key() % 10

        term, _ = Term.objects.get_or_create(
            year=academic_term.year, quarter=quarter_int)
        return term


class Term(models.Model):
    WINTER = 1
    SPRING = 2
    SUMMER = 3
    AUTUMN = 4

    QUARTER_CHOICES = (
        (WINTER, 'WIN'), (SPRING, 'SPR'), (SUMMER, 'SUM'), (AUTUMN, 'AUT')
    )

    SWS_LABELS = {
        WINTER: 'winter', SPRING: 'spring', SUMMER: 'summer', AUTUMN: 'autumn'}

    year = models.SmallIntegerField()
    quarter = models.SmallIntegerField(choices=QUARTER_CHOICES)

    objects = TermManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'quarter'],
                                    name='unique_term')
        ]

    @property
    def name(self):
        return '{}{}'.format(
            dict(self.QUARTER_CHOICES).get(self.quarter), self.year)

    def json_data(self):
        return {
            'id': self.pk,
            'year': self.year,
            'quarter': dict(self.QUARTER_CHOICES).get(self.quarter),
        }

    def next(self):
        sws_term = get_term_by_year_and_quarter(
            self.year, self.SWS_LABELS.get(self.quarter))
        nexterm = next_term(sws_term)

        quarter_int = nexterm.int_key() % 10
        term, _ = Term.objects.get_or_create(
            year=nexterm.year, quarter=quarter_int)
        return term
