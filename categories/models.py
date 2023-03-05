from django.db import models
from common.models import CommonModel

# tutorial의 태그 ex) fullstack, frontend, backend, design, devops
# class TutorialTag:
#     name = models.CharField(max_length=50)
#     user = models.ForeignKey(
#         "tutorials.Tutorial",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="tutorial_tags"  # reverse url 설정
#     )    

#     def __str__(self) -> str:
#         return f"{self.name}"
    

class Category(CommonModel):
    """Room or Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
