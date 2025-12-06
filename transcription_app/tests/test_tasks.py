from unittest.mock import patch
from rest_framework.test import APITestCase
from transcription_app.models import Transcript, ActionItem
from transcription_app.ai_tasks import generate_summary_and_tasks
from scheduler_app.models import Meeting
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskExtractionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="123456")
        self.meeting = Meeting.objects.create(title="T", organizer=self.user)
        self.transcript = Transcript.objects.create(
            meeting=self.meeting, transcript_text="John will update API by Friday."
        )

    @patch("transcription_app.services.task_extractor.extract_tasks")
    @patch("transcription_app.services.summary_generator.generate_structured_summary")
    def test_task_generation(self, mock_sum, mock_tasks):
        mock_sum.return_value = {
            "key_points": ["KP"],
            "decisions": ["OK"],
            "risks": [],
            "deadlines": [],
            "full_summary": "x"
        }
        mock_tasks.return_value = [
            {"description": "Update API", "owner": "John", "deadline": "2025-01-10"}
        ]

        generate_summary_and_tasks(self.meeting.id)

        items = ActionItem.objects.filter(meeting=self.meeting)
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().owner, "John")
