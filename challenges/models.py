from django.db import models

# 도전 정보를 담을 모델
class Challenge(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=50)  # 새로운 category 필드 추가
    description = models.TextField()
    main_image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
        on_delete=models.CASCADE,
        related_name="evaluation_criterials"
    )
    item_description = models.TextField(
        max_length=100)  # "Item Description" 칼럼 추가

    # 다른 필드들도 추가 가능

    def __str__(self):
        return self.item_description


class EvaluationResult(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    challenger = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="+")
    evaluator = models.ForeignKey(
        "users.User", on_delete=models.CASCADE)
    criteria = models.ForeignKey(
        EvaluationCriteria, on_delete=models.CASCADE, related_name="+")

    # 선택 옵션 정의
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Undecided', 'Undecided'),
    ]

    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='Pass',  # 기본값 설정 (예: 'Pass')
    )

    def __str__(self):
        return f"{self.participant}'s evaluation result: {self.get_result_display()}"


class Challenger(models.Model):
    challenge = models.ManyToManyField(Challenge, related_name='challengers')
    challenger = models.OneToOneField(
        "users.User", on_delete=models.CASCADE)
    evaluation_results = models.ManyToManyField(
        EvaluationResult, related_name='challenger_results'
    )
