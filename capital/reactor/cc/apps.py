from django.apps import AppConfig


class CcConfig(AppConfig):
    name = 'cc'

    def ready(self):
        from . import signals
