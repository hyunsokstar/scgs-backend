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
        return f"{self.title} written by {self.writer.username}"

    class Meta:
        ordering = ['-id']


class CoWriterForStudyNote(models.Model):
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        # related_name="co_writeres"
    )
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="note_cowriters"
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.writer.username} <=> {self.study_note.title}의 공동 저자"


class StudyNoteContent(models.Model):
    class ContentOptionChoices(models.TextChoices):
        SUBTITLE_FOR_PAGE = ("subtitle_for_page ", "페이지 서브 타이틀")
        NOTE_CONTENT = ("note_content", "노트 내용")
        YOUTUBE = ("youtube", "youtube content")

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

    order = models.IntegerField(default=1)


    page = models.IntegerField(default=1)

    content_option = models.CharField(
        max_length=20,
        choices=ContentOptionChoices.choices,
        default=ContentOptionChoices.NOTE_CONTENT,
    )

    ref_url1 = models.URLField(blank=True)
    ref_url2 = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
