from core.models import Task
from core.serializers import TaskSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['post'])
    def progress(self, request, pk=None):
        task = self.get_object()
        task.state = task.IN_PROGRESS
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
