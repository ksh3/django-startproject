from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class User(AbstractUser):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        UNANSERED = 'unansered', _('Unansered')

    nickname = models.CharField(
        _("Nickname"), max_length=255, blank=True,
        validators=[
            validators.MinLengthValidator(4), validators.MaxValueValidator(255)
        ]
    )
    gender = models.CharField(
        max_length=9,
        choices=Gender.choices,
        default=Gender.UNANSERED,
    )
    birthday = models.DateField(_('Birthday'), blank=True, null=True)

    def __str__(self) -> str:
        return self.username

    # FIXME: Define subscriber.
    @property
    def is_subscriber(self) -> bool:
        return False
