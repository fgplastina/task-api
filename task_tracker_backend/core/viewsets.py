from core.models import Task
from core.serializers import (
    ReadOnlyTaskSerializer,
    StateSummarySerializer,
    TaskSerializer,
)
from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self, *args, **kwargs):
        serializer = super().get_serializer_class(*args, **kwargs)

        if self.action == "progress" or self.action == "complete":
            serializer = ReadOnlyTaskSerializer

        return serializer

    @action(detail=True, methods=["post"])
    def progress(self, request, pk=None):
        # Validar estado futuro
        task = self.get_object()

        if task.state == task.COMPLETED_STATE:
            return Response(
                f"{task}({task.id}) is in state {task.COMPLETED_STATE}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if task.state == task.IN_PROGRESS_STATE:
            return Response(
                f"{task}({task.id}) is already in state {task.IN_PROGRESS_STATE}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(task)
        task.progress()
        task.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.state == task.COMPLETED_STATE:
            return Response(
                f"{task}({task.id}) is already in state {task.COMPLETED_STATE}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if task.state == task.PLANNED_STATE:
            return Response(
                f"{task}({task.id}) is in state {task.PLANNED_STATE}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        task.complete()
        task.save()

        return Response(serializer.data)


class StateSummaryAPIView(viewsets.ViewSet):
    queryset = Task.objects.all()
    serializer_class = StateSummarySerializer

    def list(self, request):
        planned_hours = (
            Task.objects.filter(state=Task.PLANNED_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        in_progress_hours = (
            Task.objects.filter(state=Task.IN_PROGRESS_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        completed_hours = (
            Task.objects.filter(state=Task.COMPLETED_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        summary_data = {
            "planned_hours": planned_hours,
            "in_progress_hours": in_progress_hours,
            "completed_hours": completed_hours,
        }

        serializer = StateSummarySerializer(summary_data)

        return Response(serializer.data)
