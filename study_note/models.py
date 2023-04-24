from django.db import models
from django.utils import timezone

class StudyNote(models.Model):
    title = models.CharField(max_length=30, default='black')
    description = models.TextField(default='black')

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="study_notes",
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    

class StudyNoteContent(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="note_contents"
    )    

    title = models.CharField(max_length=30, default='black')
    file_name = models.CharField(max_length=50, null=True, blank=True)

    content = models.TextField(default='black')

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )    

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

