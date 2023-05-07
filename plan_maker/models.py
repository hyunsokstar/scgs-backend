from django.db import models
from django.utils import timezone
# from datetime import datetime


class LongTermPlan(models.Model):
    class TaskCategoryChoices(models.TextChoices):
        PROJECT = ("project", "project 일정")
        STUDY = ("study", "study 일정")
        EVENT = ("event", "event 일정")

    title = models.CharField(max_length=30, default='미정')
    description = models.CharField(max_length=50, default='미정')

    category = models.CharField(
        max_length=10,
        choices=TaskCategoryChoices.choices,
        default=TaskCategoryChoices.PROJECT  # 기본값을 "month"로 설정
    )

    writer = models.ForeignKey(
            "users.User",
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            related_name="long_term_plans",
        )
    
    created_at = models.DateTimeField(default=timezone.now)