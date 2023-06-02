from django.db import models
from common.models import CommonModel

# Create your models here.
class TestResultImageForTask(CommonModel):
    test = models.ForeignKey(
        "project_progress.TestForTask",
        on_delete=models.CASCADE,
        max_length=200,
        null=True,
        blank=True,
        related_name="test_result_images"
    )
    image_url = models.URLField()

class TestResultImageForExtraTask(CommonModel):
    test = models.ForeignKey(
        "project_progress.TestForExtraTask",
        on_delete=models.CASCADE,
        max_length=200,
        null=True,
        blank=True,
        related_name="test_result_images"
    )
    image_url = models.URLField()    

class ReferImageForTask(CommonModel):
    image_url = models.URLField()
    task = models.ForeignKey(
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        max_length=200,
        null=True,
        blank=True,
        related_name="task_images"
    )


class PhotoForProfile(CommonModel):
    file = models.URLField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profileImages"  # 이후 출력할때 reverse url 로 접근하기 위해 필요
    )


class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(max_length=140,)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos"
    )
    
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"
