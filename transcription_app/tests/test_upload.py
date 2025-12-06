import io
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from scheduler_app.models import Meeting
from transcription_app.models import Transcript
from django.contrib.auth import get_user_model


User = get_user_model()


class UploadAudioTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="123456")
        self.client.force_authenticate(self.user)
        self.meeting = Meeting.objects.create(
            title="Test", description="x", organizer=self.user
        )

    def test_upload_audio_success(self):
        url = f"/api/transcription/{self.meeting.id}/upload/"
        audio = io.BytesIO(b"fakeaudio")
        audio.name = "test.wav"

        response = self.client.post(url, {"audio_file": audio}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transcript_id = response.data["transcript_id"]
        self.assertTrue(Transcript.objects.filter(id=transcript_id).exists())

    def test_upload_without_file(self):
        url = f"/api/transcription/{self.meeting.id}/upload/"
        res = self.client.post(url)
        self.assertEqual(res.status_code, 400)
