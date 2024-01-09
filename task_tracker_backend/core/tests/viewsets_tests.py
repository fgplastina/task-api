from core.models import Task
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


class TaskViewSetTest(TestCase):
    BASE_URL = "/api/tasks/"

    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            name="Test Task",
            description="Description for test task",
            estimated=timezone.timedelta(hours=2),
            state=Task.PLANNED_STATE,
        )
        self.task_url = f"/api/tasks/{self.task.id}/"

    def test_get_task_list(self):
        response = self.client.get(self.BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_detail(self):
        response = self.client.get(self.task_url)
        response_data = response.json()
        print(response_data)
        task_data = {
            "id": response_data.get("id"),
            "name": "Test Task",
            "description": "Description for test task",
            "estimated": "02:00:00",
            "state": "planned",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(task_data, response_data)

    #
    def test_create_task(self):
        data = {
            "name": "New Task",
            "description": "Description for new task",
            "estimated": "22:00:00",
        }
        response = self.client.post(self.BASE_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_progress_action(self):
        response = self.client.post(f"{self.task_url}progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.state, Task.IN_PROGRESS_STATE)

    def test_complete_action(self):
        self.task.state = Task.IN_PROGRESS_STATE
        self.task.save()
        response = self.client.post(f"{self.task_url}complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.state, Task.COMPLETED_STATE)
