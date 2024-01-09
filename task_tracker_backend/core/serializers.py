from core.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    estimated = serializers.DurationField(required=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "estimated",
            "state",
            "created_date",
        )
        read_only_fields = [
            "state",
            "created_date",
        ]


class ReadOnlyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "estimated",
            "state",
            "created_date",
        )
        read_only_fields = [
            "id",
            "name",
            "description",
            "estimated",
            "state",
            "created_date",
        ]


class StateSummarySerializer(serializers.Serializer):
    planned_hours = serializers.DurationField()
    in_progress_hours = serializers.DurationField()
    completed_hours = serializers.DurationField()
