from django.db import models
from common.models import CommonModel

# Create your models here.

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
    # file = models.FileField()
    file = models.URLField()            
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"


