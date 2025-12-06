from datetime import datetime, timedelta
from django.utils import timezone
from tasks_app.models import Task
from notifications_app.services.email_service import send_email

def send_task_reminders():
    now = timezone.now()

    # 24 hour reminders
    soon = now + timedelta(hours=24)
    tasks_24 = Task.objects.filter(deadline__range=[now, soon], status="todo")

    for task in tasks_24:
        if task.owner and task.owner.email:
            subject = f"Reminder: Task due in 24 hours"
            body = f"Task: {task.description}\nDeadline: {task.deadline}"
            send_email(task.owner.email, subject, body)

    # 1 hour reminders
    soon = now + timedelta(hours=1)
    tasks_1 = Task.objects.filter(deadline__range=[now, soon], status="todo")

    for task in tasks_1:
        if task.owner and task.owner.email:
            subject = f"Urgent Reminder: Task due in 1 hour"
            body = f"Task: {task.description}\nDeadline: {task.deadline}"
            send_email(task.owner.email, subject, body)

    # Overdue
    overdue = Task.objects.filter(deadline__lt=now, status="todo")

    for task in overdue:
        if task.owner and task.owner.email:
            subject = f"Task Overdue Alert"
            body = f"Task: {task.description}\nWas due: {task.deadline}"
            send_email(task.owner.email, subject, body)
            send_slack_message(f"Summary for meeting '{meeting.title}' is ready.")

