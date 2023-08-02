import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parser_project.settings')
app = Celery('parser_project', backend='rpc://', broker='amqp://localhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
