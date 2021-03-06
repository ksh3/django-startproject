import logging

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from . models import User

logger = logging.getLogger(__name__)


class RegistrationForm(UserCreationForm):

    username = forms.EmailField(
        label=_('Username'), help_text=_('Email'))

    class Meta:
        model = User
        fields = ('username', )
        field_classes = {'username': UsernameField}
