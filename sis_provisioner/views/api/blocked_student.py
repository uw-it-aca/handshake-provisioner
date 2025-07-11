# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from sis_provisioner.views.api import APIView
from sis_provisioner.models import BlockedHandshakeStudent
from uw_saml.utils import get_user
from datetime import datetime, timezone
from logging import getLogger
import json

logger = getLogger(__name__)


class BlockedStudentListView(APIView):
    def get(self, request, *args, **kwargs):
        students = BlockedHandshakeStudent.objects.all().order_by(
            '-added_date')
        data = [s.json_data() for s in students]
        return self.json_response(data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body).get('student', {})
        username = data.get('username').strip().lower()
        reason = data.get('reason').strip()

        blocked_student, _ = BlockedHandshakeStudent.objects.get_or_create(
            username=username, defaults={
                'added_by': get_user(request),
                'added_date': datetime.now(timezone.utc),
                'reason': reason,
            })
        return self.json_response(blocked_student.json_data())


class BlockedStudentView(APIView):
    def delete(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        try:
            student = BlockedHandshakeStudent.objects.get(pk=student_id)
            student.delete()
            return self.json_response(status=204)
        except BlockedHandshakeStudent.DoesNotExist:
            return self.error_response(404, 'Not Found')
