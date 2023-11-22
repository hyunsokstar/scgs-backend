from django.db import models

# title,
# product,
# manager,
# email,
# phone_number,
# content
# estimate_require_completion
# memo

class Estimate(models.Model):
    class RequireCompletionChoices(models.TextChoices):
        complete = ("complete", "완료")
        uncomplete = ("uncomplete", "비완료")

    title = models.CharField(
        max_length=180,
        default="",
    )

    product = models.CharField(max_length=50, default="")
    manager = models.CharField(max_length=80, default="")
    email = models.CharField(max_length=80, default="")
    phone_number = models.CharField(max_length=50, default="")
    content = models.TextField(default=True)


    estimate_require_completion = models.CharField(
        max_length=20,
        choices=RequireCompletionChoices.choices
    )

    memo = models.TextField(default=True)

    def __str__(self) -> str:
        return self.title