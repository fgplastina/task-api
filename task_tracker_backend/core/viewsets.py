from datetime import timedelta

from core.models import Task
from core.serializers import (
    ReadOnlyTaskSerializer,
    StateSummarySerializer,
    TaskSerializer,
)
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
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

        serializer = self.get_serializer(task)
        task.complete()
        task.save()

        return Response(serializer.data)


class StateSummaryAPIView(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = StateSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_date"]

    def get_queryset(self):
        queryset = super(StateSummaryAPIView, self).get_queryset()
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        if start_date and end_date:
            queryset = queryset.filter(
                created_date__range=[start_date, end_date]
            )

        return queryset

    def list(self, request):
        qs = self.get_queryset()

        duration_zero = timedelta(days=0, hours=0, minutes=0, seconds=0)

        planned_hours = (
            qs.filter(state=Task.PLANNED_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        in_progress_hours = (
            qs.filter(state=Task.IN_PROGRESS_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        completed_hours = (
            qs.filter(state=Task.COMPLETED_STATE)
            .aggregate(Sum("estimated"))
            .get("estimated__sum")
        )

        summary_data = {
            "planned_hours": planned_hours or duration_zero,
            "in_progress_hours": in_progress_hours or duration_zero,
            "completed_hours": completed_hours or duration_zero,
        }

        serializer = StateSummarySerializer(summary_data)

        return Response(serializer.data)
