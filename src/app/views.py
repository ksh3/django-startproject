import logging

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from . import forms, decorators

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


@method_decorator([login_required], 'dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'


@method_decorator([login_required, decorators.subscriber_required], 'dispatch')
class PaidContentView(TemplateView):
    template_name = 'paid-content.html'


@method_decorator([login_required], 'dispatch')
class FreeContentView(TemplateView):
    template_name = 'free-content.html'


class RegistrationView(CreateView):
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('app:login')
    template_name = 'registration.html'


class InheritedLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self) -> str:
        url = self.get_redirect_url()
        return url or reverse_lazy('app:dashboard')
