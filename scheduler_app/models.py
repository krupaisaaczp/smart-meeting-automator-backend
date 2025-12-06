from django.db import models
from auth_app.models import User
import uuid

class Meeting(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_meetings")
    participants = models.ManyToManyField(User, related_name="meetings")

    scheduled_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)

    meeting_link = models.URLField(null=True, blank=True)
    calendar_event_id = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
