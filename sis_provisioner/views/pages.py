# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from sis_provisioner.models.term import Term
from uw_saml.utils import get_user
from django.urls import reverse


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
        context['signOutUrl'] = reverse('saml_logout')
        return context
