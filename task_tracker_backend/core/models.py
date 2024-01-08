from django.db import models

# Create your models here.

class TaskState:
    def transition_to(self, task):
        raise Exception("Not implement yet")


    def __str__(self):
        pass

class PlannedState(TaskState):
    def transition_to(self, task):
        task.state = InProgressState()

    def __str__(self):
        return "Planned"

class InProgressState(TaskState):
    def transition_to(self, task):
        task.state = CompletedState()

    def __str__(self):
        return "In Progress"

class CompletedState(TaskState):
    def transition_to(self, task):
        raise Exception(f"task {task} in {task.COMPLETED_STATE} state cannot be transitioned to a different state.")


    def __str__(self):
        return "Completed"


class Task(models.Model):
    PLANNED_STATE = "planned"
    IN_PROGRESS_STATE = "in_progress"
    COMPLETED_STATE = "completed"

    STATE_CHOICES = [
        (PLANNED_STATE, "Planned"),
        (IN_PROGRESS_STATE, "In Progress"),
        (COMPLETED_STATE, "Completed"),
    ]

    name = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    estimated = models.DurationField()
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default="planned"
    )

    def __str__(self):
        return self.name
