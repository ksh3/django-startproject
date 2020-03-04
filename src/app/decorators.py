import logging
import functools

from django.core.exceptions import PermissionDenied


logger = logging.getLogger(__name__)


def subscriber_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_subscriber:
            return fn(*args, **kwargs)
        raise PermissionDenied

    return wrapper
