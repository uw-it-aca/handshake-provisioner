# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView
from sis_provisioner.views.pages import DefaultPageView
from sis_provisioner.views.pages import PageView


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
    # add default Vue page routes here
    # re_path(r"^(customize|page2|page3)$", DefaultPageView.as_view()),
    re_path(r"^$", DefaultPageView.as_view()),
]
