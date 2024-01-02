# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.exceptions import ObjectDoesNotExist
from sis_provisioner.views.api import APIView
from sis_provisioner.models import HandshakeStudentsFile, Term
from uw_saml.utils import get_user
import json


class FileListView(APIView):
    def get(self, request, *args, **kwargs):
        files = HandshakeStudentsFile.objects.all().order_by('-created_date')
        data = [f.json_data() for f in files]
        return self.json_response(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body).get('file', {})
        term_str = data.get('academic_term')
        is_test_file = data.get('is_test_file', True)

        if term_str == 'current':
            term = Term.objects.current()
        elif term_str == 'next':
            term = Term.objects.next()
        else:
            return self.error_response(400, 'Invalid term')

        import_file = HandshakeStudentsFile(term=term,
                                            is_test_file=is_test_file,
                                            created_by=get_user(request))
        import_file.save()
        return self.json_response(import_file.json_data())


class FileView(APIView):
    def get(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')

        try:
            import_file = HandshakeStudentsFile.objects.get(pk=file_id)
            return self.file_response(import_file.content,
                                      import_file.filename)
        except HandshakeStudentsFile.DoesNotExist:
            return self.error_response(404, 'Not Found')
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')

    def put(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')

        try:
            import_file = HandshakeStudentsFile.objects.get(pk=file_id)
            import_file.sisimport()
            return self.json_response(content=import_file.json_data())
        except HandshakeStudentsFile.DoesNotExist:
            return self.error_response(404, 'Not Found')
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')
        except Exception as ex:
            return self.error_response(500, ex)

    def delete(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')

        try:
            import_file = HandshakeStudentsFile.objects.get(pk=file_id)
            import_file.delete()
            return self.json_response(status=204)
        except HandshakeStudentsFile.DoesNotExist:
            return self.error_response(404, 'Not Found')
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')
