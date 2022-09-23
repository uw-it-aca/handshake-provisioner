# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from sis_provisioner.models import ImportFile
from logging import getLogger
import json
import re

logger = getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class APIView(View):
    @staticmethod
    def json_response(content='', status=200):
        return HttpResponse(json.dumps(content, sort_keys=True),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def error_response(status, message='', content={}):
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


class FileListView(APIView):
    def get(self, request, *args, **kwargs):
        files = ImportFile.objects.all().order_by('-created_date')
        data = [f.json_data() for f in files]
        return self.json_response(data)

    def post(self, request, *args, **kwargs):
        academic_term = request.data.get('academic_term')
        is_test_file = request.data.get('is_test_file', True)

        try:
            import_file = ImportFile.objects.add_file(academic_term,
                                                      is_test_file)
        except Exception:
            pass # TODO

        return self.json_response(import_file.json_data())


class FileView(APIView):
    def get(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')

        try:
            import_file = ImportFile.objects.get(pk=file_id)
        except ImportFile.DoesNotExist:
            return self.error_response(404, 'Not Found')

        try:
            return self.file_response(import_file.content,
                                      import_file.filename)
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')
