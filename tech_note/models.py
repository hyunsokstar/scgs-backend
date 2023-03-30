from django.db import models
from django.utils import timezone


class TechNote(models.Model):
    class CATEGORY_CHOICES(models.TextChoices):
        create = ("create", "Create")
        read = ("read", "Read")
        update = ("update", "Update")
        delete = ("delete", "Delete")
        boiler_plate = ("boiler_plate", "BoilerPlate")
        library_example = ("libray_example", "LibraryExample")

    author = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="tech_notes"
    )
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES.choices,
        blank=True,
        null=True
    )
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
