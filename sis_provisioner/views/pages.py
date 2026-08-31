# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from uw_saml.utils import get_user

from sis_provisioner.models.term import Term


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response({"context_data": context})

    def get_context_data(self, **kwargs):
        context = {}
        context['currentTerm'] = Term.objects.current().name
        context['nextTerm'] = Term.objects.next().name
        context['userName'] = get_user(self.request)
        context['handshakeFilesUrl'] = reverse('handshake-file-list')
        context['uconnectFilesUrl'] = reverse('uconnect-file-list')
        context['handshakeBlockedUrl'] = reverse('handshake-blocked-list')
        context['uconnectBlockedUrl'] = reverse('uconnect-blocked-list')
        context['signOutUrl'] = reverse('saml_logout')
        return context
