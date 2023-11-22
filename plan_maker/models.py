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

    def __str__(self):
        return '%s: %s' % (self.title, self.category)

class LongTermPlanContents(models.Model):

    class PlanTypeChoices(models.TextChoices):
        PROJECT = 'project', 'Project'
        TASK = 'task', 'Task'
        MILESTONE  = 'milestone', 'Milestone'

    long_term_plan = models.ForeignKey(
        "plan_maker.LongTermPlan",
        on_delete=models.CASCADE,
        related_name="contents",
        blank=True,
        null=True,
    )

    start = models.DateField()
    end = models.DateField()
    name = models.CharField(max_length=255) # 일정 이름
    progress = models.IntegerField() # 일정 진행률
    displayOrder = models.IntegerField() # 정렬 순서
    dependencies = models.TextField(null=True, blank=True) # 어떤 일정과 연결 되는지 

    def __str__(self):
        return self.name    