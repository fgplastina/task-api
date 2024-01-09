import datetime

from django.db import models
from django_fsm import FSMField, transition


class Task(models.Model):
    PLANNED_STATE = "planned"
    IN_PROGRESS_STATE = "in progress"
    COMPLETED_STATE = "completed"

    STATE_CHOICES = [
        (PLANNED_STATE, PLANNED_STATE),
        (IN_PROGRESS_STATE, IN_PROGRESS_STATE),
        (COMPLETED_STATE, COMPLETED_STATE),
    ]

    created_date = models.DateTimeField()
    name = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    estimated = models.DurationField()
    state = FSMField(choices=STATE_CHOICES, default=PLANNED_STATE)

    def __str__(self):
        return self.name.capitalize()

    def save(
        self,
        *args,
        **kwargs
    ):
        self.created_date = datetime.datetime.now()
        return super().save(*args, **kwargs)

    @transition(field=state, source=PLANNED_STATE, target=IN_PROGRESS_STATE)
    def progress(self):
        pass

    @transition(field=state, source=IN_PROGRESS_STATE, target=COMPLETED_STATE)
    def complete(self):
        pass
