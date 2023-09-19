from django.db import models

# Create your models here.
# python manage.py makemigrations
# python manage.py migrate
class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="surveys"
    )

    def __str__(self):
        return self.title

class SurveyOption(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_options')
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content

class SurveyAnswer(models.Model):
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.writer.username}'s answer to {self.survey.title}"
