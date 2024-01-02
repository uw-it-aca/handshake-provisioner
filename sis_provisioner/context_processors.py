# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from uw_saml.utils import get_user
from django.urls import reverse


def auth_user(request):
    return {
        'username': get_user(request),
        'signout_url': reverse('saml_logout'),
    }


def google_analytics(request):
    return {'google_analytics': getattr(settings, 'GOOGLE_ANALYTICS_KEY', ' ')}


def django_debug(request):
    return {'django_debug': getattr(settings, 'DEBUG', False)}
