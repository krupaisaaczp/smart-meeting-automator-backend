from rest_framework.test import APITestCase
from transcription_app.models import Transcript
from scheduler_app.models import Meeting
from django.contrib.auth import get_user_model


User = get_user_model()


class TranscriptStatusTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="123456")
        self.client.force_authenticate(self.user)
        self.meeting = Meeting.objects.create(title="T", organizer=self.user)
        self.transcript = Transcript.objects.create(meeting=self.meeting)

    def test_status_success(self):
        url = f"/api/transcription/status/{self.transcript.id}/"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("status", res.data)
