from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "API.settings")

app = Celery("API")
# app.config_from_object('django.conf:settings', namespace='CELERY')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task
def debug_task(namedemo):
    print "=========",namedemo


debug_task.delay('aniket')