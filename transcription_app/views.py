from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .ai_tasks import generate_summary_and_tasks


from .models import Summary
from .serializers import SummarySerializer

from .models import Transcript
from .services.storage import save_local_file
from .tasks import process_audio_transcription
from scheduler_app.models import Meeting

class UploadAudioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meeting_id):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found"}, status=404)

        file_obj = request.FILES.get("audio_file")
        if not file_obj:
            return Response({"error": "audio_file required"}, status=400)

        local_path = save_local_file(file_obj, filename=file_obj.name)

        transcript, created = Transcript.objects.update_or_create(
            meeting=meeting,
            defaults={
                "uploaded_filename": file_obj.name,
                "local_file_path": local_path,
                "processing_status": "pending"
            }
        )

        process_audio_transcription.delay(str(transcript.id))

        return Response({"transcript_id": transcript.id}, status=201)




class GetSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, meeting_id):
        try:
            summary = Summary.objects.get(meeting__id=meeting_id)
        except Summary.DoesNotExist:
            return Response({"error":"No summary found"}, status=404)
        return Response(SummarySerializer(summary).data)


class TranscriptStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transcript_id):
        try:
            transcript = Transcript.objects.get(id=transcript_id)
        except Transcript.DoesNotExist:
            return Response({"error": "Transcript not found"}, status=404)

        return Response({
            "id": str(transcript.id),
            "meeting_id": str(transcript.meeting.id) if transcript.meeting else None,
            "status": transcript.processing_status,
            "text_available": bool(transcript.transcript_text),
            "external_id": transcript.external_id
        })

from .models import ActionItem
from rest_framework import status

class GetTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, meeting_id):
        tasks = ActionItem.objects.filter(meeting__id=meeting_id)
        data = [
            {
                "id": str(t.id),
                "description": t.description,
                "owner": t.owner,
                "deadline": t.deadline,
                "status": t.status
            }
            for t in tasks
        ]
        return Response(data)
