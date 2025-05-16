# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_sws import sws_now
from datetime import datetime


def current_datetime():
    override_dt = getattr(settings, "CURRENT_DATETIME_OVERRIDE", None)
    if override_dt is not None:
        return datetime.strptime(override_dt, "%Y-%m-%d %H:%M:%S")
    else:
        return sws_now()
