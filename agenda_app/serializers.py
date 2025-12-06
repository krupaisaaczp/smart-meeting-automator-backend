from rest_framework import serializers
from .models import Agenda

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = "__all__"
        read_only_fields = ["id", "version", "created_at", "updated_at"]
