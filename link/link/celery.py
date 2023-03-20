import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'link.settings')
django.setup()

celery_app = Celery('link')
celery_app.config_from_object('django.conf:settings', namespace="CELERY")
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
