# -*- coding: utf-8 -*-
from django.apps import AppConfig


class KobraConfig(AppConfig):
    name = 'kobra'
    verbose_name = 'Kobra'

    def ready(self):
        # Imports the permissions module to make sure the rules are loaded
        from . import permissions

        # This will make sure the app is always imported when Django starts so
        # that shared_task will use this app.
        from .tasks import celery_app


default_app_config = 'kobra.KobraConfig'
