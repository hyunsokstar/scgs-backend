from django.db import models
from django.utils import timezone  # 날짜 및 시간 관련 유틸리티 임포트


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

    created_at = models.DateTimeField(
        default=timezone.now)  # 생성 날짜와 시간을 저장하는 필드
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SurveyOption(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='survey_options')
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


class SurveyAnswer(models.Model):
    participant = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="survey_answers"
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE , related_name='survey_answers')
    selected_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.participant.username}'s answer to {self.survey.title}"
