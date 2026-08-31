# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import json
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class APIView(View):
    @staticmethod
    def json_response(content='', status=200):
        return HttpResponse(json.dumps(content, sort_keys=True),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def error_response(status, message='', content=None):
        if content is None:
            content = {}
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def file_response(content, filename, content_type='text/csv'):
        response = HttpResponse(content=content, status=200,
                                content_type=content_type)

        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            re.sub(r'[,/]', '-', filename))

        return response
