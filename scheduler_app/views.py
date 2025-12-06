from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services.trigger_parser import TriggerParser
from .services.scheduler_service import SchedulerService
from .serializers import MeetingSerializer
from auth_app.models import User
from dateparser import parse as parse_date
from .services.calendar_service import CalendarService
from rest_framework import generics
from .models import Meeting


class MeetingListCreateView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer



class TriggerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text", "")
        parser = TriggerParser()
        result = parser.parse(text)

        return Response(result)


class ScheduleMeetingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MeetingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        meeting = serializer.save(organizer=request.user)

        service = CalendarService(request.user)

        slot = service.find_available_slots(
            meeting.participants.all(),
            meeting.duration_minutes
        )

        meeting.scheduled_time = slot
        meeting.save()

        updated_meeting = service.create_event(meeting)

        return Response(MeetingSerializer(updated_meeting).data)
