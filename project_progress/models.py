from django.db import models
from django.utils import timezone
# from pytz import timezone as tz

from datetime import datetime

# Create your models here.
# seoul_tz = tz('Asia/Seoul')
# timezone.activate(seoul_tz)


class ProjectProgress(models.Model):
    class TaskStatusChoices(models.TextChoices):
        uncomplete = ("uncomplete", "비완료")
        complete = ("complete", "완료")

    task_manager = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="progect_tasks",
        blank=True,
        null=True
    )

    task = models.CharField(max_length=50, default="")
    writer = models.CharField(max_length=80, blank=True, null=True)
    importance = models.IntegerField(default=1, blank=True, null=True)

    task_completed = models.BooleanField(default=False)

    password = models.CharField(max_length=20, default=True)
    started_at_utc = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    due_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)

    @property
    def started_at(self):
        return timezone.localtime(self.started_at_utc)

    def __str__(self) -> str:
        return self.task

    def completed_at_formatted(self):
        local_completed_at = timezone.localtime(self.completed_at)
        completed_at_str = ""
        if (self.completed_at == None):
            completed_at_str = "미정"
        else:
            completed_at_str = self.completed_at.strftime(
                '%y년 %m월 %d일 %H시 %M분')
            print("completed_at_str : ", completed_at_str)

        return completed_at_str

        print("custom time : ", self.completed_at.strftime('%y년 %m월 %d일 %H시 %M분'))
        return self.completed_at.strftime('%y년 %m월 %d일 %H시 %M분')

    def started_at_formatted(self):
        print("custom time : ", self.started_at.strftime('%y년 %m월 %d일 %H시 %M분'))
        return self.started_at.strftime('%y년 %m월 %d일 %H시 %M분')

    def due_date_formatted(self):
        local_due_date = self.due_date
        print("local_due_date : ", local_due_date)
        due_date_str = ""
        if (local_due_date == None or local_due_date == ""):
            due_date_str = "미정"
        else:
            due_date_str = local_due_date.strftime('%y년 %m월 %d일 %H시 %M분')
            print("due_date_str : ", due_date_str)

        return due_date_str

    def elapsed_time_from_started_at(self):
        started_at = timezone.localtime(self.started_at_utc)
        now = timezone.now()
        elapsed_time_minutes = round(
            (now - started_at).total_seconds() / 60)  # 총 몇분

        # 분(minute) 단위로 계산한 값을 시간(hour)과 분(minute)으로 변환
        hours, minutes = divmod(elapsed_time_minutes, 60)

        # 시간 분 형식의 문자열로 변환
        elapsed_time_str = f"{hours}시간 {minutes}분"

        return elapsed_time_str

    def time_consumed_from_start_to_complete(self):

        if (self.started_at_utc != None and self.completed_at != None):
            started_at = timezone.localtime(self.started_at_utc)
            completed_at = self.completed_at
            elapsed_time_minutes = round(
                (completed_at - started_at).total_seconds() / 60)  # 총 몇분

            # 분(minute) 단위로 계산한 값을 시간(hour)과 분(minute)으로 변환
            hours, minutes = divmod(elapsed_time_minutes, 60)

            # 시간 분 형식의 문자열로 변환
            time_consumed_from_startat_to_completed_str = f"{hours}시간 {minutes}분"

            return time_consumed_from_startat_to_completed_str
        else:
            return "미정"

    def time_left_to_due_date(self):
        due_date = timezone.localtime(self.due_date)
        now = timezone.now()
        time_left_to_due_date = round(
            (due_date - now).total_seconds() / 60)  # 총 몇분

        # 분(minute) 단위로 계산한 값을 시간(hour)과 분(minute)으로 변환
        hours, minutes = divmod(time_left_to_due_date, 60)

        # 시간 분 형식의 문자열로 변환
        time_left_to_due_date_str = f"{hours}시간 {minutes}분"

        return time_left_to_due_date_str
