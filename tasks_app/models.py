import uuid
from django.db import models
from scheduler_app.models import Meeting
from auth_app.models import User

class Task(models.Model):
    STATUS_CHOICES = (("todo","To Do"),("in_progress","In Progress"),("done","Done"))
    PRIORITY_CHOICES = (("low","Low"),("medium","Medium"),("high","High"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="tasks")
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner_email = models.EmailField(null=True, blank=True)   # helpful if owner not in user table
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    confidence_score = models.FloatField(default=0.0)
    external_sync_id = models.CharField(max_length=255, null=True, blank=True)
    external_system = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


