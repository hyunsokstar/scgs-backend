from django.db import models
from django.utils import timezone


class RoadMap(models.Model):
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="loadmaps",
    )
    title = models.CharField(max_length=50)
    sub_title = models.CharField(max_length=50)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title}"


class StudyNote(models.Model):
    class FirstCategoryChoices(models.TextChoices):
        FRONTEND = ("frontend", "Frontend")
        BACKEND = ("backend", "Backend")
        FULLSTACK = ("full-stack", "FullStack")

    class SecondCategoryChoices(models.TextChoices):
        TUTORIAL = ("tutorial", "Tutorial")
        FRAMEWORK = ("framework", "Framework")
        LIBRARY = ("library", "Library")
        BOILER_PLATE = ("boiler-plate", "Boiler Plate")
        SAMPLE_CODE = ("sample-code", "Sample Code")
        CODE_REVIEW = ("code-review", "Code Review")
        PROGRAMMING_LANGUAGE = ("programming-language", "Programming Language")
        CHALLENGE = ("challenge", "Challenge")

    title = models.CharField(max_length=80, default="black")
    description = models.TextField(default="black", blank=True, null=True)

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="study_notes",
    )
    created_at = models.DateTimeField(default=timezone.now)

    first_category = models.CharField(
        max_length=20,
        choices=FirstCategoryChoices.choices,
        default=FirstCategoryChoices.FRONTEND,
    )
    second_category = models.CharField(
        max_length=20,
        choices=SecondCategoryChoices.choices,
        default=SecondCategoryChoices.TUTORIAL,
    )

    # view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} written by {self.writer.username}"

    class Meta:
        ordering = ["-id"]


class LikeForStudyNote(models.Model):
    user = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="study_note_likes",
    )

    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    liked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Like by {self.user.username} for {self.study_note.title}"


class BookMarkForStudyNote(models.Model):
    user = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="study_note_bookmarks",
    )

    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    bookmarked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"bookmark by {self.user.username} for {self.study_note.title}"


class RoadMapContent(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+",
    )

    road_map = models.ForeignKey(
        "study_note.RoadMap",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="contents",
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order = models.IntegerField(default=1)

    created_at = models.DateTimeField(default=timezone.now)


class ErrorReportForStudyNote(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="error_report_list",
    )
    page = models.PositiveIntegerField(default=1)

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    content = models.TextField(null=True, blank=True)

    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.content} for {self.study_note.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class CommentForErrorReport(models.Model):
    error_report = models.ForeignKey(
        "ErrorReportForStudyNote", on_delete=models.CASCADE, related_name="comments"
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"댓글 - {self.error_report.study_note.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class QnABoard(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="question_list",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    page = models.PositiveIntegerField(default=1)
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class AnswerForQaBoard(models.Model):
    question = models.ForeignKey(
        "study_note.QnABoard",
        on_delete=models.CASCADE,
        related_name="answers_for_qa_board",
    )
    content = models.TextField()
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class ClassRoomForStudyNote(models.Model):
    current_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="class_list",
    )
    current_page = models.PositiveIntegerField(default=1)
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


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
        related_name="note_cowriters",
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_tasking = models.BooleanField(default=False)
    current_page = models.IntegerField(null=True, blank=True)
    task_description = models.CharField(
        max_length=30, default="", null=True, blank=True
    )

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
        related_name="note_contents",
    )

    title = models.CharField(max_length=30, default="black")
    file_name = models.CharField(max_length=50, null=True, blank=True)

    content = models.TextField(default="black")

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order = models.IntegerField(default=1)

    page = models.IntegerField(default=1)

    content_option = models.TextField(
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


class StudyNoteBriefingBoard(models.Model):
    note = models.ForeignKey(
        "study_note.StudyNote",
        on_delete=models.CASCADE,
        related_name="note_comments",
        blank=True,
        null=True,
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="study_note_comments",
    )

    comment = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_edit_mode = models.BooleanField(default=False)

    def created_at_formatted(self):
        if self.created_at != None:
            local_created_at = timezone.localtime(self.created_at)
            return local_created_at.strftime("%y년 %m월 %d일 %H 시 %M분")
        else:
            return "준비"


class FAQBoard(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="faq_list",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class CommentForFaqBoard(models.Model):
    faq_board = models.ForeignKey(
        "study_note.FaqBoard",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments_list",
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"내용: {self.content}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")


class Suggestion(models.Model):
    study_note = models.ForeignKey(
        "study_note.StudyNote",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="suggestion_list",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m%d%H%M")


class CommentForSuggestion(models.Model):
    suggestion = models.ForeignKey(
        "study_note.Suggestion",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments_list",
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"내용: {self.content}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime("%m월 %d일 %H시 %M분")
