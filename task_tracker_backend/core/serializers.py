from core.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    estimated = serializers.DurationField(required=True)
    class Meta:
        model = Task
        fields = ("name", "description", "estimated")
