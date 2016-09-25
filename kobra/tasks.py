# -*- coding: utf-8 -*-
from django.conf import settings

from celery import Celery, shared_task

celery_app = Celery('kobra')

celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
