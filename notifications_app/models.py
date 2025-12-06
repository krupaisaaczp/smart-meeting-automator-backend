from django.db import models
from scheduler_app.models import Meeting
from tasks_app.models import Task
from auth_app.models import User
import uuid

class NotificationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, null=True, blank=True, on_delete=models.SET_NULL)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50)  # summary_email, task_reminder, overdue_alert
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="sent")
