from unittest.mock import patch
from rest_framework.test import APITestCase
from scheduler_app.models import Meeting
from transcription_app.models import Transcript, Summary, ActionItem
from transcription_app.tasks import process_audio_transcription
from django.contrib.auth import get_user_model


User = get_user_model()


class PipelineTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="123456")
        self.meeting = Meeting.objects.create(title="X", organizer=self.user)
        self.transcript = Transcript.objects.create(
            meeting=self.meeting,
            local_file_path="/tmp/audio.wav",
            processing_status="pending",
        )

    @patch("transcription_app.services.speech_to_text.AssemblyAIService.poll")
    @patch("transcription_app.services.speech_to_text.AssemblyAIService.request_transcription")
    @patch("transcription_app.services.speech_to_text.AssemblyAIService.upload_audio")
    @patch("transcription_app.ai_tasks.generate_summary_and_tasks.delay")
    def test_full_pipeline(
        self, mock_gen, mock_upload, mock_req, mock_poll
    ):
        mock_upload.return_value = "url://uploaded"
        mock_req.return_value = "abc123"
        mock_poll.return_value = {
            "text": "Test meeting transcript",
            "words": [],
            "utterances": []
        }

        process_audio_transcription(self.transcript.id)

        self.transcript.refresh_from_db()
        self.assertEqual(self.transcript.processing_status, "completed")
        mock_gen.assert_called_once()
def test_requires_auth(self):
    self.client.force_authenticate(user=None)
    url = f"/api/transcription/{self.meeting.id}/upload/"
    res = self.client.post(url)
    self.assertEqual(res.status_code, 401)
