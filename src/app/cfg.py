from django.apps import AppConfig as BaseConfig


class AppConfig(BaseConfig):
    label = 'app'
    name = 'src.app'
    verbose_name = 'app'

    def ready(self):
        from . import signals
