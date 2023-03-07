from django.db import models

# tutorial_images: FileList;
# title: string;
# price: string;
# frontend_framework_option: string;
# backend_framework_option: string;
# description: string;
# teacher: string;
# tutorial_url: string;


class Tutorial(models.Model):
    class BckendFrameWorkOption(models.TextChoices):
        django_drf = ("django_drf", "django_drf")
        fast_api = ("fast_api", "fast_api")
        spring_boot = ("sptring_boot", "spring_boot")
        express = ("express", "express")
        nest_js = ("nest_js", "nest_js")

    class FrontEndFrameWorkOption(models.TextChoices):
        react = ("react", "react")
        svelte = ("svelte", "svelte")
        flutter = ("flutter", "flutter")

    author = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    tutorial_image = models.URLField(null=True, blank=True)

    title = models.CharField(
        max_length=100,
        default="",
    )

    teacher = models.CharField(
        max_length=25,
        default="",
    )

    price = models.CharField(
        max_length=20,
        default="",
    )

    description = models.TextField(default="", blank=True, null=True)
    tutorial_url = models.URLField(null=True, blank=True)

    backend_framework_option = models.CharField(
        max_length=20,
        choices=BckendFrameWorkOption.choices,
        null=True,
        blank=True
    )

    frontend_framework_option = models.CharField(
        max_length=20,
        choices=FrontEndFrameWorkOption.choices,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.title
