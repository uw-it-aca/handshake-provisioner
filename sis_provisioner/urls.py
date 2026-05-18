# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView
from sis_provisioner.views.pages import HomeView
from sis_provisioner.views.api.file.handshake import (
    HandshakeFileListView, HandshakeFileView)
from sis_provisioner.views.api.file.uconnect import (
    UconnectFileListView, UconnectFileView)
from sis_provisioner.views.api.blocked_student import (
    BlockedStudentListView, BlockedStudentView)

urlpatterns = []


# add debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^500$",
            TemplateView.as_view(template_name="500.html"),
            name="500_response",
        ),
        re_path(
            r"^404$",
            TemplateView.as_view(template_name="404.html"),
            name="404_response",
        ),
    ]

urlpatterns += [
    re_path(r"^api/v1/handshake/file$",
            HandshakeFileListView.as_view(), name="handshake-file-list"),
    re_path(r"^api/v1/handshake/file/(?P<file_id>[\d]+)$",
            HandshakeFileView.as_view(), name="handshake-file"),
    re_path(r"^api/v1/uconnect/file$",
            UconnectFileListView.as_view(), name="uconnect-file-list"),
    re_path(r"^api/v1/uconnect/file/(?P<file_id>[\d]+)$",
            UconnectFileView.as_view(), name="uconnect-file"),
    re_path(r"^api/v1/blocked-student/?$",
            BlockedStudentListView.as_view(), name="blocked-student-list"),
    re_path(r"^api/v1/blocked-student/(?P<student_id>[\d]+)$",
            BlockedStudentView.as_view(), name="blocked-student"),
    # vue-router paths
    re_path(r"^(blocked-student|uconnect-files).*$", HomeView.as_view()),
    # default landing
    re_path(r"^$", HomeView.as_view(), name="index"),
]
