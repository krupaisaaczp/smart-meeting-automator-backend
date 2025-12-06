from rest_framework.test import APITestCase
from transcription_app.models import Summary
from scheduler_app.models import Meeting
from django.contrib.auth import get_user_model


User = get_user_model()


class SummaryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="123456")
        self.client.force_authenticate(self.user)

        self.meeting = Meeting.objects.create(title="T", organizer=self.user)
        self.summary = Summary.objects.create(
            meeting=self.meeting,
            key_points=["A", "B"],
            decisions=["D"],
            full_summary="Test summary"
        )

    def test_get_summary(self):
        url = f"/api/transcription/{self.meeting.id}/summary/"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["full_summary"], "Test summary")
