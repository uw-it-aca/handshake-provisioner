# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import re

from memcached_clients import RestclientPymemcacheClient

ONE_DAY = 60 * 60 * 24


class RestClientsCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'sws' == service and re.match(r'^/student/v\d/term/\d{4}', url):
            return ONE_DAY
