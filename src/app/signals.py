import logging
import threading

from django.utils import timezone
import requests
from django.conf import settings
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver


logger = logging.getLogger(__name__)
