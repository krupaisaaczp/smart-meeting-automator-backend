from django.db import models
from scheduler_app.models import Meeting
import uuid

class Agenda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE)

    generated_content = models.TextField()
    edited_content = models.TextField(null=True, blank=True)

    version = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agenda for {self.meeting.title}"
