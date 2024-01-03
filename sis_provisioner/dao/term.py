# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from sis_provisioner.dao import current_datetime
from uw_sws.term import get_term_by_date, get_term_after


def current_term():
    return get_term_by_date(current_datetime().date())


def next_term():
    return get_term_after(current_term())
