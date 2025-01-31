# encoding: utf-8

'''🤐 Zipperlab task queues using Celery.'''

from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jpl.labcas.zipper.policy.settings.ops')
app = Celery('Zipperlab')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
