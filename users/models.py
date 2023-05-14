from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import CommonModel

# Create your models here.


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMAIL = ("female", "Female")

    class PositionChoices(models.TextChoices):
        frontend = "frontend", "FrontEnd"
        backend = "backend", "BackEnd"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    admin_level = models.IntegerField(default=1)

    name = models.CharField(max_length=150, default="")

    position = models.ForeignKey(
        "users.UserPosition",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    about_me = models.TextField(null=True, blank=True)

    skill_for_frameWork = models.ManyToManyField(
        "users.SkillForFrameWork",
        related_name="users",
        null=True,
        blank=True,
    )

    profile_image = models.URLField(null=True, blank=True)
    cash = models.IntegerField(default=0)

    # 스터디 노트 콘텐츠 리스트 에디터 모드
    is_edit_mode_for_study_note_contents = models.BooleanField(default=False)
    task_in_progress = models.CharField(max_length=50, default="crud 작업중")

class UserPosition(CommonModel):
    position_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.position_name}"

    class Meta:
        verbose_name_plural = "UserPosition"


class SkillForFrameWork(CommonModel):
    frame_work_name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.frame_work_name}"

    class Meta:
        verbose_name_plural = "SkillForFrameWork"

# 파이썬 활용 능력 + 문서화
# 노트로 정리 + git 공유

# 샘플 프로젝트로 증명 해라 (아마존 연동)

# textbox
# 개발 환경 구축 능력
# 홈페이지 구축 능력
# 쇼핑몰 구축 능력
# 라이브 스트리밍 + 채팅 + 결제
# 스마트 팩토리 + iot

# css
# 기본 css, scss
# react
#
# chakra ui 활용 능력

# 알고리즘 능력
# 페이지 네이션 알고리즘 구현 능력

# user에 대해 추가해야 할 정보 (체크 박스로 선택할 것들)
# SkilForFrameWork : django drf, fastapi, nest js, spring boot, react
# SkillForSql : sql , django orm, prisma, jpa
# SkilForDb: mysql, postgre, mongo, sqlite
# skilnotefordevops render aws azure cloudflare s3 docker
# MyFavoriteSubject (homepage, shoppingmall, live streaming, chatting, iot)
# skilDocu(note 사이트에의 프로필 페이지 링크,  종합 점수(노트 평점) , 대표 서비스 링크 )
