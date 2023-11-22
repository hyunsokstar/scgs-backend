from django.db import models


class ApiDocu(models.Model):
    class ClassificationChoices(models.TextChoices):
        FRONT = 'front', 'Frontend'
        BACK = 'back', 'Backend'

    classification = models.CharField(
        max_length=10,
        choices=ClassificationChoices.choices,
    )
    url = models.URLField(max_length=50)
    description = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="api_docus",
    )

    def __str__(self):
        return self.url
