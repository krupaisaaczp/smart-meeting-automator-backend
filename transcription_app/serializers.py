from rest_framework import serializers
from .models import Summary


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = [
            "id",
            "meeting",
            "key_points",
            "decisions",
            "risks",
            "deadlines",
            "full_summary",
            "created_at",
        ]
