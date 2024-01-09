from core.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    estimated = serializers.DurationField(required=True)
#    state = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Task
        fields = ("id", "name", "description", "estimated", "state")
        read_only_fields = ["state", ]


class ReadOnlyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "name", "description", "estimated", "state")
        read_only_fields = ["id", "name", "description", "estimated", "state"]


class StateSummarySerializer(serializers.Serializer):
    planned_hours = serializers.DurationField()
    in_progress_hours = serializers.DurationField()
    completed_hours = serializers.DurationField()
