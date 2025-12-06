from celery import shared_task
from .models import Transcript, Summary
from transcription_app.services.summarizer import extract_decisions_and_actions, chunk_text
from tasks_app.services.task_extractor import create_tasks_from_actions

@shared_task(bind=True)
def generate_summary_and_tasks(self, meeting_id):
    try:
        transcript = Transcript.objects.get(meeting__id=meeting_id)
    except Transcript.DoesNotExist:
        return {"error":"transcript not found"}

    text = transcript.transcript_text or ""
    if not text:
        return {"error": "empty transcript"}

    # extract decisions and actions
    parsed = extract_decisions_and_actions(text)
    decisions = parsed.get("decisions", [])
    actions = parsed.get("actions", [])

    # create or update Summary object
    summary, created = Summary.objects.update_or_create(
        meeting=transcript.meeting,
        defaults={
            "full_summary": (text[:4000] if len(text)>4000 else text),
            "decisions": decisions,
            "key_points": [],   # could add future heuristics
            "risks": [],
            "deadlines": [a.get("deadline") for a in actions if a.get("deadline")]
        }
    )

    # create tasks
    created_tasks = create_tasks_from_actions(transcript.meeting, actions)
    
    send_meeting_summary(meeting)

    return {
        "summary_id": str(summary.id),
        "tasks_created": len(created_tasks)
    }

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
