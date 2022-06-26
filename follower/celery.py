from __future__ import absolute_import, unicode_literals
import os
import logging
from django.conf import settings
from celery.schedules import crontab
# from .config import create_api

# from .utils import msg_followers
from celery import Celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'follower.settings')

app = Celery('folower')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# celery -A follower beat -l info --logfile=celery.beat.log --detach
# celery -A follower worker -l info --logfile=celery.log -P solo --detach
# celery -A follower beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=celery.beat.log