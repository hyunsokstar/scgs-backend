from django.db import models
from django.utils import timezone

# 챌린지
class Challenge(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=50)  # 새로운 category 필드 추가
    description = models.TextField()
    main_image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    started_at = models.DateTimeField(default=timezone.now)  # 현재 날짜 및 시간을 기본값으로 설정
    deadline = models.DateTimeField(default=timezone.now)    # 현재 날짜 및 시간을 기본값으로 설정

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

# 챌린지에 대한 평가 기준 (예를 들어 item_description 이 얼굴, 몸매, 성격)
class EvaluationCriteria(models.Model):
    challenge = models.ForeignKey(
        Challenge,  # Challenge 모델 가르킴
        on_delete=models.CASCADE,
        related_name="evaluation_criterials"
    )
    item_description = models.CharField(
        max_length=100)  # "Item Description" 칼럼 추가

    # 다른 필드들도 추가 가능

    def __str__(self):
        return self.item_description


# 평가 기준들에 대한 결과
class EvaluationResult(models.Model):
    challenger = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+"
    )
    
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
        related_name='evaluations'
    )

    # challenge_result = models.OneToOneField(
    #     "challenges.ChallengeResult",
    #     on_delete=models.CASCADE,
    #     related_name="challenge_result",
    #     null=True,  
    #     blank=True
    # )

    evaluate_criteria_description = models.CharField(
        max_length=100,
        default="",  # 빈 문자열을 기본값으로 설정
    )

    # 선택 옵션 정의
    RESULT_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('undecided', 'Undecided'),
    ]

    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='Pass',  # 기본값 설정 (예: 'Pass')
    )

    def __str__(self):
        return f"{self.challenger}'s evaluation result: {self.get_result_display()}"

# 최종적 평가 결과와 comment
class ChallengeResult(models.Model):

    challenger = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+"
    )

    challenge = models.ForeignKey(
        Challenge,  # Challenge 모델과 연결
        on_delete=models.CASCADE,
        related_name="challenge_results"
    )
    pass_status = models.BooleanField(default=False)  # 합격 여부를 나타내는 칼럼
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def created_at_formatted(self):
        return self.created_at.strftime('%y년 %m월 %d일')