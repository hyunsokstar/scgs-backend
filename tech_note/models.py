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

    task = models.ForeignKey(
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        related_name="related_notes",
        blank=True,
        null=True,
    )

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

    @property
    def note_content_count(self):
        return self.tech_note_contents.count()


class TechNoteContent(models.Model):
    tech_note = models.ForeignKey(
        "tech_note.TechNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="tech_note_contents"
    )
    note_content_title = models.CharField(max_length=50)
    note_content_file = models.CharField(max_length=50, null=True, blank=True)
    note_content_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


