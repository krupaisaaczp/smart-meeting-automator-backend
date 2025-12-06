from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_meeting_automator.settings')

app = Celery('smart_meeting_automator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    # Runs every hour
    "send-task-reminders-every-hour": {
        "task": "notifications_app.tasks.run_task_reminders",
        "schedule": crontab(minute=0),
    },
}
