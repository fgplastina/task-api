from django.test import TestCase
from django.utils import timezone

from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="Test Task",
            description="Description for test task",
            estimated=timezone.timedelta(hours=2),
            state=Task.PLANNED_STATE,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Description for test task")
        self.assertEqual(self.task.estimated, timezone.timedelta(hours=2))
        self.assertEqual(self.task.state, Task.PLANNED_STATE)

    def test_task_str_representation(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_task_progress_transition(self):
        self.task.progress()
        self.assertEqual(self.task.state, Task.IN_PROGRESS_STATE)

    def test_task_complete_transition(self):
        self.task.state = Task.IN_PROGRESS_STATE
        self.task.save()

        self.task.complete()
        self.assertEqual(self.task.state, Task.COMPLETED_STATE)

    def test_invalid_transition(self):
        # Change task default state to an invalid one
        self.task.state = Task.COMPLETED_STATE
        self.task.save()
        with self.assertRaises(Exception):
            self.task.progress()

    def test_invalid_complete_transition(self):
        # Task is already en planned state 
        with self.assertRaises(Exception):
            self.task.complete()
