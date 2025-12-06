from celery import shared_task
from transcription_app.models import Transcript, Summary, ActionItem
from transcription_app.services.summary_generator import generate_structured_summary
from transcription_app.services.task_extractor import extract_tasks



@shared_task
def generate_summary_and_tasks(meeting_id):
    try:
        transcript = Transcript.objects.get(meeting__id=meeting_id)
    except Transcript.DoesNotExist:
        return

    if not transcript.transcript_text:
        return

    # 1. Generate structured summary
    summary_data = generate_structured_summary(transcript.transcript_text)

    Summary.objects.update_or_create(
        meeting=transcript.meeting,
        defaults={
            "key_points": summary_data.get("key_points", []),
            "decisions": summary_data.get("decisions", []),
            "risks": summary_data.get("risks", []),
            "deadlines": summary_data.get("deadlines", []),
            "full_summary": summary_data.get("full_summary", "")
        }
    )

    # 2. Extract actionable tasks
    task_list = extract_tasks(transcript.transcript_text)

    # delete previous AI tasks
    ActionItem.objects.filter(meeting=transcript.meeting).delete()

    for task in task_list:
        ActionItem.objects.create(
            meeting=transcript.meeting,
            description=task["description"],
            owner=task.get("owner"),
            deadline=task.get("deadline")
        )
        
        task_list = extract_tasks(transcript.transcript_text)

        # clear existing tasks
        ActionItem.objects.filter(meeting=transcript.meeting).delete()

        for task in task_list:
            ActionItem.objects.create(
                meeting=transcript.meeting,
                description=task.get("description"),
                owner=task.get("owner"),
                deadline=task.get("deadline")
            )

