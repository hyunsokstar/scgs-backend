
from django.db import models
from django.utils import timezone
from datetime import datetime
import pytz
from datetime import timedelta


class ProjectProgress(models.Model):    
    class TaskClassificationChoices(models.TextChoices):
        CRUD = ("crud", "CRUD 작업")
        NEW_FUTURE = ("new-future", "새로운 기능 개발")
        TROUBLE_SHOOTING = ("trouble-shooting", "문제 해결 작업")
        UI_TASK = ("ui-task", "UI 작업")
        REFACTORING = ("refactoring", "리팩토링 작업")
        OPTIMIZATION = ("optimization", "최적화 작업")
        BOILTER_PATE = ("boiler-plate", "보일러 플레이트 만들기")
        TEST_CODE = ("test-code", "테스트 코드 작성")

    class TaskStatusChoices(models.TextChoices):
        ready = ("ready", "준비")
        in_progress = ("in_progress", "작업중")
        testing = ("testing", "테스트중")
        completed = ("completed", "완료")

    class TimeOptionChoices(models.TextChoices):
        MORNING_TASKS = 'morning_tasks', '아침 작업'
        AFTERNOON_TASKS = 'afternoon_tasks', '오후 작업'
        NIGHT_TASKS = 'night_tasks', '밤 작업'

    task_manager = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="progect_tasks",
    )

    task = models.CharField(max_length=80, default="")
    order = models.IntegerField(default=None, null=True, blank=True)

    # 마감일
    due_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    
    # morning_tasks afternoon_tasks 
    # due_date_option = models.CharField(max_length=20, default="")
    due_date_option = models.CharField(
        max_length=20,
        choices=TimeOptionChoices.choices,
        default=TimeOptionChoices.MORNING_TASKS,
    )

    task_description = models.TextField(max_length=300, default="")

    task_classification = models.CharField(
        max_length=20,
        choices=TaskClassificationChoices.choices,
        default=TaskClassificationChoices.CRUD,
    )

    writer = models.CharField(max_length=50, blank=True, null=True)
    importance = models.IntegerField(default=1, blank=True, null=True)

    in_progress = models.BooleanField(default=False)
    is_testing = models.BooleanField(default=False)
    task_completed = models.BooleanField(default=False)
    check_result_by_tester = models.BooleanField(default=False)

    is_task_for_urgent = models.BooleanField(default=False)
    check_for_cash_prize = models.BooleanField(default=False)

    score_by_tester = models.IntegerField(default=0, null=True, blank=True)

    is_success_for_cash_prize = models.BooleanField(default=False)

    current_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.ready  # 기본값을 "ready"로 설정
    )

    password = models.CharField(max_length=20, default=True)
    created_at = models.DateTimeField(default=timezone.now)
    started_at_utc = models.DateTimeField(null=True, blank=True, default=None)
    completed_at = models.DateTimeField(blank=True, null=True)

    cash_prize = models.IntegerField(default=0)
    is_urgent_request = models.BooleanField(default=False)
    is_task_for_cash_prize = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = ProjectProgress.objects.all().aggregate(models.Max('order'))['order__max']
            if max_order is None:
                self.order = 1
            else:
                self.order = max_order + 1
        super().save(*args, **kwargs)

    @property
    def started_at(self):
        return timezone.localtime(self.started_at_utc)

    def __str__(self) -> str:
        return self.task

    def completed_at_formatted(self):
        local_completed_at = timezone.localtime(self.completed_at)
        completed_at_str = ""
        if (self.completed_at == None):
            completed_at_str = "미정"
        else:
            completed_at_str = local_completed_at.strftime(
                '%y년 %m월 %d일 %H시 %M분')
            print("completed_at_str : ", completed_at_str)

        return completed_at_str

    def started_at_formatted(self):
        if (self.started_at_utc != None):
            local_started_at = timezone.localtime(self.started_at_utc)
            return local_started_at.strftime('%y년 %m월 %d일 %H시 %M분')
        else:
            return "미정"

    def due_date_formatted(self, client_timezone='Asia/Seoul'):
        if self.due_date is None:
            return "미정"

        local_due_date = timezone.localtime(self.due_date)
        local_due_date = pytz.timezone(
            client_timezone).normalize(local_due_date)
        due_date_str = local_due_date.strftime('%y년 %m월 %d일 %H시 %M분')
        print("due_date_str : ", due_date_str)
        return due_date_str

    def elapsed_time_from_started_at(self):
        started_at = timezone.localtime(self.started_at_utc)
        now = timezone.now()
        elapsed_time_minutes = round(
            (now - started_at).total_seconds() / 60)  # 총 몇분

        # 분(minute) 단위로 계산한 값을 시간(hour)과 분(minute)으로 변환
        hours, minutes = divmod(elapsed_time_minutes, 60)

        # 시간 분 형식의 문자열로 변환
        elapsed_time_str = f"{hours}시간 {minutes}분"

        return elapsed_time_str

    def time_consumed_from_start_to_complete(self):

        if (self.started_at_utc != None and self.completed_at != None):
            started_at = timezone.localtime(self.started_at_utc)
            completed_at = self.completed_at
            elapsed_time_minutes = round(
                (completed_at - started_at).total_seconds() / 60)  # 총 몇분

            # 분(minute) 단위로 계산한 값을 시간(hour)과 분(minute)으로 변환
            hours, minutes = divmod(elapsed_time_minutes, 60)

            # 시간 분 형식의 문자열로 변환
            time_consumed_from_startat_to_completed_str = f"{hours}시간 {minutes}분"

            return time_consumed_from_startat_to_completed_str
        else:
            return "미정"

    def time_left_to_due_date(self, client_timezone='Asia/Seoul'):
        time_left_to_due_date_str = ""
        print("self.due_date ::::::::::::::::::::::::::::", self.due_date   )

        if self.due_date is not None and self.started_at_utc is not None:
            # 로컬 타임존으로 변환
            local_due_date = timezone.localtime(self.due_date)
            local_started_at = timezone.localtime(self.started_at_utc)

            # 시간 차이 계산
            time_left = local_due_date - local_started_at

            # 응답 문자열 생성
            if time_left.total_seconds() < 0:
                hours, seconds = divmod(abs(time_left).seconds, 3600)
                minutes = seconds // 60
                time_left_to_due_date_str = f"{hours}시간 {minutes}분 초과"
            else:
                days, remainder = divmod(time_left.total_seconds(), 86400)
                hours, seconds = divmod(remainder, 3600)
                minutes = (seconds % 3600) // 60
                if days > 0:
                    time_left_to_due_date_str = f"{int(days)}일 {int(hours)}시간 {int(minutes)}분 남음"
                else:
                    time_left_to_due_date_str = f"{int(hours)}시간 {int(minutes)}분 남음"

        return time_left_to_due_date_str


class ExtraTask(models.Model):
    class TaskStatusChoices(models.TextChoices):
        ready = ("ready", "준비")
        in_progress = ("in_progress", "작업중")
        testing = ("testing", "테스트중")
        completed = ("completed", "완료")

    original_task = models.ForeignKey(
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        related_name="extra_tasks",
        blank=True,
        null=True,
    )

    task_manager = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="task_manager_for_supplementary_task",
    )

    task = models.TextField(default="", blank=True, null=True)
    task_status = models.CharField(
        max_length=20,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.ready  # 기본값을 "ready"로 설정
    )

    importance = models.IntegerField(default=1, blank=True, null=True)
    password = models.CharField(max_length=20, default="1234")

    started_at = models.DateTimeField(null=True, blank=True, default=None)
    completed_at = models.DateTimeField(blank=True, null=True)

    due_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        return self.task

    def completed_at_formatted(self):
        local_completed_at = timezone.localtime(self.completed_at)
        completed_at_str = ""
        if (self.completed_at == None):
            completed_at_str = "미정"
        else:
            completed_at_str = local_completed_at.strftime(
                '%y년 %m월 %d일 %H시 %M분')
            print("completed_at_str : ", completed_at_str)

        return completed_at_str

    def started_at_formatted(self):
        if (self.started_at != None):
            local_started_at = timezone.localtime(self.started_at)
            return local_started_at.strftime('%y년 %m월 %d일 %H시 %M분')
        else:
            return "준비"


class TestForTask(models.Model):
    class TestMethodChoices(models.TextChoices):
        browser = ("browser", "브라우져")
        postman = ("postman", "postman")
        test_code = ("test_code", "test_code")

    original_task = models.ForeignKey(                  # 어떤 태스크의 테스트
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        related_name="tests_for_tasks",
        blank=True,
        null=True,
    )

    test_description = models.CharField(max_length=50, default="")
    test_passed = models.BooleanField(default=False)

    test_method = models.CharField(
        max_length=20,
        choices=TestMethodChoices.choices,
        default=TestMethodChoices.browser  # 기본값을 "ready"로 설정
    )

    test_result_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.test_description


class TestersForTest(models.Model):
    test = models.ForeignKey(                  # 어떤 태스크의 테스트
        "project_progress.TestForTask",
        on_delete=models.CASCADE,
        related_name="testers_for_test",
        blank=True,
        null=True,
    )

    tester = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class ChallengersForCashPrize(models.Model):
    task = models.ForeignKey(                  # 어떤 태스크의 테스트
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        related_name="challegers_for_cach_prize",
        blank=True,
        null=True,
    )

    challenger = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class TaskComment(models.Model):
    task = models.ForeignKey(
        "project_progress.ProjectProgress",
        on_delete=models.CASCADE,
        related_name="task_comments",
        blank=True,
        null=True,
    )

    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="task_comments",
    )

    comment = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    is_edit_mode = models.BooleanField(default=False)

    def created_at_formatted(self):
        if (self.created_at != None):
            local_created_at = timezone.localtime(self.created_at)
            return local_created_at.strftime('%y년 %m월 %d일 %H시 %M분')
        else:
            return "준비"

class TaskLog(models.Model):
    taskPk = models.IntegerField(default=0)
    writer = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="task_logs",
    )
    task = models.CharField(max_length=80, default="")
    completed_at = models.DateTimeField(default=timezone.now)
    interval_between_team_task = models.DurationField(blank=True, null=True)
    interval_between_my_task = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # 이전 row와의 차이 시간 계산
            previous_task_log = TaskLog.objects.order_by('-completed_at').first()

            if previous_task_log:
                time_difference = timezone.now() - previous_task_log.completed_at
                self.interval_between_team_task = time_difference  # timedelta 객체를 그대로 저장

            # 작성자가 같을 경우의 차이 시간 계산
            previous_task_log_same_writer = TaskLog.objects.filter(writer=self.writer).order_by('-completed_at').first()

            if previous_task_log_same_writer:
                time_difference_same_writer = timezone.now() - previous_task_log_same_writer.completed_at
                self.interval_between_my_task = time_difference_same_writer  # timedelta 객체를 그대로 저장

        super().save(*args, **kwargs)


    # @property
    # def interval_between_team_task_timedelta(self):
    #     if self.interval_between_team_task is not None:
    #         return self.interval_between_team_task  # timedelta 객체 그대로 반환
    #     return None

