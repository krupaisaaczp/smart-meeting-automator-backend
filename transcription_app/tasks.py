from celery import shared_task
from .models import Transcript
from .services.speech_to_text import AssemblyAIService
from .ai_tasks import generate_summary_and_tasks


@shared_task(bind=True, max_retries=3)
def process_audio_transcription(self, transcript_id):
    transcript = Transcript.objects.get(id=transcript_id)
    transcript.processing_status = "processing"
    transcript.save()

    try:
        svc = AssemblyAIService()

        # 1. Upload local file
        upload_url = svc.upload_audio(transcript.local_file_path)

        # 2. Request transcription
        transcript_id_remote = svc.request_transcription(upload_url)
        transcript.external_id = transcript_id_remote
        transcript.save()

        # 3. Poll
        result = svc.poll(transcript_id_remote)

        # 4. Persist results
        transcript.transcript_text = result.get("text")
        transcript.word_count = len((result.get("text") or "").split())
        transcript.timestamps = result.get("words", [])
        transcript.speaker_labels = result.get("utterances", [])
        transcript.processing_status = "completed"
        transcript.save()

        # 5. AUTO–GENERATE SUMMARY + TASKS
        generate_summary_and_tasks.delay(str(transcript.meeting.id))

    except Exception as e:
        transcript.processing_status = "failed"
        transcript.save()
        raise self.retry(exc=e, countdown=5)
