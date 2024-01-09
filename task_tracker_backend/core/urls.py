from core.viewsets import StateSummaryAPIView, TaskViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(
    r"tasks-summary", StateSummaryAPIView, basename="tasks-summary"
)


urlpatterns = [
    path("api/", include(router.urls)),
]
