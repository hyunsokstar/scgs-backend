from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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

    description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    classification = models.CharField(
        max_length=10,
        choices=ClassificationChoices.choices,
    )

    tags = models.ManyToManyField(
        Tags,
        related_name='shortcuts',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

class RelatedShortcut(models.Model):
    shortcut = models.ForeignKey(                  # 어떤 태스크의 테스트
        "shortcut.ShortCut",
        on_delete=models.CASCADE,
        related_name="related_shortcut_list",
        blank=True,
        null=True,
    )
    shortcut_content = models.TextField(max_length=500, null=True, blank=True)
    description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.shortcut_content



class ShortCutHub(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="shortcut_hubs",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class ShortCutHubContent(models.Model):
    shortcut = models.ForeignKey(
        "shortcut.ShortCut",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    
    shortcut_hub = models.ForeignKey(
        "shortcut.ShortCutHub",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="contents"
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order = models.IntegerField(default=1)

    created_at = models.DateTimeField(default=timezone.now)
    