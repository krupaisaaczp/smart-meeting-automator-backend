from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Agenda
from .serializers import AgendaSerializer
from .services.agenda_generator import AgendaGenerator
from scheduler_app.models import Meeting


class GenerateAgendaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meeting_id):
        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found"}, status=404)

        generator = AgendaGenerator()
        content = generator.generate(meeting)

        agenda, created = Agenda.objects.update_or_create(
            meeting=meeting,
            defaults={
                "generated_content": content,
                "version": 1,
            }
        )

        return Response(AgendaSerializer(agenda).data)


class UpdateAgendaView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, meeting_id):
        try:
            agenda = Agenda.objects.get(meeting_id=meeting_id)
        except Agenda.DoesNotExist:
            return Response({"error": "Agenda not found"}, status=404)

        edited_content = request.data.get("edited_content")

        if not edited_content:
            return Response({"error": "edited_content is required"}, status=400)

        agenda.edited_content = edited_content
        agenda.version += 1
        agenda.save()

        return Response(AgendaSerializer(agenda).data)
