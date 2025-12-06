from celery import shared_task
from notifications_app.services.task_reminder import send_task_reminders

@shared_task
def run_task_reminders():
    send_task_reminders()
