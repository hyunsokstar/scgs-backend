from django.db import models
from django.utils import timezone

# Create your models here.


class ProjectProgress(models.Model):
    class TaskStatusChoices(models.TextChoices):
        uncomplete = ("uncomplete", "비완료")
        complete = ("complete", "완료")

    task = models.CharField(max_length=50, default="")
    writer = models.CharField(max_length=80, default="")
    importance = models.IntegerField(default=1, blank=True, null=True)

    task_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices
    )

    password = models.CharField(max_length=20, default=True)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.task
