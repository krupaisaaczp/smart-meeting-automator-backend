import uuid
from django.db import models
from scheduler_app.models import Meeting


class Transcript(models.Model):
    PROCESSING_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name="transcript")

    uploaded_filename = models.CharField(max_length=255, null=True, blank=True)
    local_file_path = models.CharField(max_length=500, null=True, blank=True)

    transcript_text = models.TextField(null=True, blank=True)
    speaker_labels = models.JSONField(null=True, blank=True)
    timestamps = models.JSONField(null=True, blank=True)

    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS,
        default="pending"
    )

    external_id = models.CharField(max_length=255, null=True, blank=True)

    word_count = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Summary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, related_name="summary")

    key_points = models.JSONField(default=list, blank=True)
    decisions = models.JSONField(default=list, blank=True)
    risks = models.JSONField(default=list, blank=True)
    deadlines = models.JSONField(default=list, blank=True)

    full_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ActionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="action_items")

    description = models.TextField()
    owner = models.CharField(max_length=255, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("completed", "Completed")],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
