from django.db import models

# Create your models here.
class ProjectProgress(models.Model):
    class TaskStatusChoices(models.TextChoices):
        # request = ("request", "요청")
        # proceeding = ("proceeding", "진행")
        uncomplete = ("uncomplete", "비완료")
        complete = ("complete", "완료")

    task = models.CharField(max_length=50, default="")
    writer = models.CharField(max_length=80, default="")
    importance = models.CharField(max_length=80, default="")

    task_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices
    )

    password = models.CharField(max_length=20,default=True)

    def __str__(self) -> str:
        return self.task
    
    # task
    # writer 
    # importance
    # task_status
    # password