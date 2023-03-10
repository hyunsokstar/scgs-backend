from django.db import models
from django.utils import timezone
from pytz import timezone as tz

from datetime import datetime

# Create your models here.
# seoul_tz = tz('Asia/Seoul')
# timezone.activate(seoul_tz)

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
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.task

    def started_at_formatted(self):
        print("custom time : ", self.started_at.strftime('%y년 %m월 %d일 %H시 %M분'))
        return self.started_at.strftime('%y년 %m월 %d일 %H시 %M분')

    def elapsed_time_from_started_at(self):
        started_at = self.started_at
        now = timezone.now()
        elapsed_time = round((now - started_at).total_seconds() / 60)  # 분 단위 계산
        return elapsed_time