# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime

from django.conf import settings
from uw_sws import sws_now


def current_datetime():
    override_dt = getattr(settings, "CURRENT_DATETIME_OVERRIDE", None)
    if override_dt is not None:
        return datetime.strptime(override_dt, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
    else:
        return sws_now()
