from django.db import models

# 도전 정보를 담을 모델
class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    subtitle = models.CharField(max_length=50)  # 새로운 category 필드 추가
    main_image = models.URLField(null=True, blank=True)

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="challenges"
    )

    def __str__(self):
        return self.title

    @property
    def created_at_formatted(self):
        return self.created_at.strftime('%y년 %m월 %d일')


class EvaluationCriteria(models.Model):
    challenge = models.ForeignKey(
        Challenge,  # Challenge 모델 가르킴
        on_delete=models.CASCADE
    )
    item_description = models.TextField(
        max_length=100)  # "Item Description" 칼럼 추가

    # 다른 필드들도 추가 가능

    def __str__(self):
        return self.item_description


class ScoreForChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    participant = models.ForeignKey(
        "users.User", related_name='scores', on_delete=models.CASCADE)
    evaluator = models.ForeignKey(
        "users.User", related_name='given_scores', on_delete=models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)

    # 선택 옵션 정의
    SCORE_CHOICES = [
        ('미정', '미정 (평가 이전)'),
        ('Excellent', '매우 훌륭 (Excellent)'),
        ('Good', '훌륭 (Good)'),
        ('Okay', '그럭저럭 (Okay)'),
        ('Insufficient', '불충분한 (Insufficient)'),
        ('Terrible', '매우 나쁜 (Terrible)'),
    ]

    result = models.CharField(
        max_length=20,
        choices=SCORE_CHOICES,
        default='미정',  # 기본값 설정 (예: '미정')
    )

    def __str__(self):
        return f"{self.participant}의 평가 결과: {self.get_result_display()}"


class Challenger(models.Model):
    participant = models.OneToOneField("users.User", on_delete=models.CASCADE)
    challenge = models.ManyToManyField(Challenge, related_name='challengers')
    challenge_scores = models.ManyToManyField(
        ScoreForChallenge,
        related_name='challengers'
    )