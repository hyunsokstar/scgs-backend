from django.db import models
from django.utils.translation import gettext_lazy as _

class ShortCut(models.Model):

    class ClassificationChoices(models.TextChoices):
        FRONT = 'front', _('Frontend')
        BACK = 'back', _('Backend')

    writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="shortcuts",
        blank=True,
        null=True,
    )

    shortcut = models.TextField(max_length=100, null=True, blank=True)

    description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    classification = models.CharField(
        max_length=10,
        choices=ClassificationChoices.choices,
    )

    def __str__(self):
        return self.shortcut
