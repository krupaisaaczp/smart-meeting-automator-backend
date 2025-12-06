from rest_framework import serializers
from scheduler_app.models import Meeting
from scheduler_app.services.google_calendar import sync_meeting_to_google
from auth_app.models import User

class MeetingSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = serializers.ListField(child=serializers.EmailField(), write_only=True)

    class Meta:
        model = Meeting
        fields = [
            "id", "title", "description", "organizer", "participants",
            "scheduled_time", "duration_minutes", "meeting_link", "status"
        ]
        read_only_fields = ["id", "meeting_link", "status"]

    def create(self, validated_data):
        participant_emails = validated_data.pop("participants")

        meeting = Meeting.objects.create(**validated_data)
        users = User.objects.filter(email__in=participant_emails)
        meeting.participants.set(users)

        # 🔥 Sync to Google Calendar + automatically attach Meet link
        sync_meeting_to_google(meeting)

        return meeting
