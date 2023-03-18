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

    task = models.CharField(max_length=50, default="")
    writer = models.CharField(max_length=80, default="")
    importance = models.IntegerField(default=1, blank=True, null=True)

    task_completed = models.BooleanField(default=False)

    password = models.CharField(max_length=20, default=True)
    started_at_utc = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    due_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)

    @property
    def started_at(self):
        return timezone.localtime(self.started_at_utc)

    def __str__(self) -> str:
        return self.task

    def started_at_formatted(self):
        print("custom time : ", self.started_at.strftime('%y년 %m월 %d일 %H시 %M분'))
        return self.started_at.strftime('%y년 %m월 %d일 %H시 %M분')
    
    def due_date_formatted(self):
        due_date_str=""
        if(self.due_date == None):
            due_date_str = "미정"
        else:
            due_date_str = self.due_date.strftime('%y년 %m월 %d일 %H시 %M분')        
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
