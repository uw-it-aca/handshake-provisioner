# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from sis_provisioner.dao import current_datetime
from uw_sws.term import (
    get_term_by_date, get_term_after, get_term_by_year_and_quarter)


def current_term():
    return get_term_by_date(current_datetime().date())


def next_term(term=None):
    if term is None:
        term = current_term()
    return get_term_after(term)
