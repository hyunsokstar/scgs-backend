from django.db import models
from django.utils import timezone

# Create your models here.


class Suggestion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="suggestion_boards"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime('%m%d%H%M')

class CommentForSuggestion(models.Model):
    suggestion = models.ForeignKey(
        "board.Suggestion",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments_list"
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="board_comments"
    )

    content = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"내용: {self.content}"

    def created_at_formatted(self):
        local_created_at = timezone.localtime(self.created_at)
        return local_created_at.strftime('%m월 %d일 %H시 %M분')        
