from rest_framework import serializers
from requests import Response
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from datetime import timedelta, datetime
import pytz

from medias.serializers import (
    ReferImageForTaskSerializer,
    TestResultImageForCompletedTaskSerializer,
    TestResultImageForTaskSerializer,
    TestResultImageForExtraTaskSerializer,
    ReferImageForExtraTaskSerializer
)

from users.serializers import (
    TinyUserSerializer,
    UserNameSerializer,
    UserProfileImageSerializer,
)
from .models import (
    ChallengersForCashPrize, ExtraTask, ExtraTaskComment,
    ProjectProgress, TaskComment, TestForTask,
    TestersForTest, TaskLog, TaskUrlForTask,
    TaskUrlForExtraTask, TestForExtraTask,
    TestersForTestForExtraTask
)

# 1122

class SerializerForAllExtraTaskList(serializers.ModelSerializer):
    class Meta:
        model = ExtraTask
        fields = [
            'id',
            'original_task',
            'task_manager',
            'task',
            'task_description',
            'task_status',
            'importance'
        ]


class CompletedTaskSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    completed_at_formatted = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    time_consumed_from_start_to_complete = serializers.SerializerMethodField()
    time_left_to_due_date = serializers.SerializerMethodField()
    task_manager = UserProfileImageSerializer()
    task_images = ReferImageForTaskSerializer(many=True)
    test_result_images = TestResultImageForCompletedTaskSerializer(many=True)

    is_for_today = serializers.SerializerMethodField()

    class Meta:
        model = ProjectProgress
        fields = (
            "id",
            "writer",
            "task",
            "task_images",
            "task_description",
            "task_manager",
            "importance",
            "is_testing",
            "in_progress",
            "task_completed",
            "current_status",
            "due_date",
            "task_classification",
            "started_at",
            "started_at_formatted",
            "completed_at",
            "completed_at_formatted",
            "due_date_formatted",
            "elapsed_time_from_started_at",
            "time_consumed_from_start_to_complete",
            "time_left_to_due_date",
            "check_result_by_tester",
            "score_by_tester",
            "is_task_for_cash_prize",
            "is_task_for_urgent",
            "cash_prize",
            'due_date_option_for_today',
            'is_for_today',
            'test_result_images'
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def completed_at_formatted(self, obj):
        return obj.completed_at_formatted()

    def get_due_date_formatted(self, obj):
        return obj.due_date_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()

    def get_time_consumed_from_start_to_complete(self, obj):
        return obj.time_consumed_from_start_to_complete()

    def get_time_left_to_due_date(self, obj):
        return obj.time_left_to_due_date()

    def get_is_for_today(self, obj):
        # 현재 시간을 현지 시간으로 설정
        local_time = timezone.localtime(timezone.now()).date()

        # obj.due_date를 현지 시간으로 변환하여 오늘과 비교
        return obj.completed_at.date() == local_time


class CreateCommentSerializerForExtraTask(ModelSerializer):

    class Meta:
        model = ExtraTaskComment
        fields = (
            "task",
            "comment",
        )


class TaskUrlForExtraTaskSerializer(ModelSerializer):
    class Meta:
        model = TaskUrlForExtraTask
        fields = ('id', 'task', 'task_url', 'task_description')


class TaskUrlForTaskSerializer(ModelSerializer):
    class Meta:
        model = TaskUrlForTask
        fields = ('id', 'task', 'task_url', 'task_description')


class TaskUrlForExtraTaskSerializer(ModelSerializer):
    class Meta:
        model = TaskUrlForExtraTask
        fields = ('id', 'task', 'task_url', 'task_description')


class ExtraTaskCommentSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer()

    class Meta:
        model = TaskComment
        fields = (
            'id',
            'task',
            'writer',
            'comment',
            'is_edit_mode',
            'like_count',
            'created_at',
            "created_at_formatted"
        )
        read_only_fields = ('id', 'created_at',)

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()


class TestersForTestForExtraTaskSerializer(serializers.ModelSerializer):
    tester = UserProfileImageSerializer()  # 필요한 경우 태스크 정보를 시리얼화

    class Meta:
        model = TestersForTestForExtraTask

        fields = (
            "pk",
            "test",
            "tester"
        )

# fix 0602


class TestForExtraTaskSerializer(ModelSerializer):
    testers_for_test_for_extra_task = TestersForTestForExtraTaskSerializer(
        many=True)
    test_result_images = TestResultImageForExtraTaskSerializer(many=True)

    class Meta:
        model = TestForExtraTask
        fields = (
            "id",
            "original_task",
            "test_description",
            "test_passed",
            "test_method",
            "test_result_images",
            "testers_for_test_for_extra_task"
        )

# fix 0612


class ExtraTasksDetailSerializer(ModelSerializer):
    task_manager = UserProfileImageSerializer()
    started_at_formatted = serializers.SerializerMethodField()
    task_urls = TaskUrlForTaskSerializer(many=True)
    task_comments = ExtraTaskCommentSerializer(many=True)
    tests_for_extra_task = TestForExtraTaskSerializer(many=True)
    task_images = ReferImageForExtraTaskSerializer(many=True)

    class Meta:
        model = ExtraTask
        fields = (
            "pk",
            "task_manager",
            "task",
            "task_description",
            "task_comments",
            "task_images",
            "tests_for_extra_task",
            "task_urls",
            "task_url1",
            "task_url2",
            "task_status",
            "importance",
            "started_at",
            "completed_at",
            "started_at_formatted"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()


class TaskLogSerializer(serializers.ModelSerializer):

    writer = UserProfileImageSerializer()
    time_distance_from_before_task = serializers.SerializerMethodField()
    time_distance_from_before_my_task = serializers.SerializerMethodField()

    def get_time_distance_from_before_task(self, instance):
        previous_task = TaskLog.objects.filter(
            completed_at__lt=instance.completed_at
        ).order_by('-completed_at').first()

        if previous_task:
            time_distance = instance.completed_at - previous_task.completed_at
            time_distance_minutes = int(
                time_distance.total_seconds() / 60)  # 시간 간격을 분 단위로 계산
            return time_distance_minutes

        return 0

    def get_time_distance_from_before_my_task(self, instance):
        previous_task = TaskLog.objects.filter(
            writer=instance.writer,
            completed_at__lt=instance.completed_at
        ).order_by('-completed_at').first()

        if previous_task:
            time_distance = instance.completed_at - previous_task.completed_at
            time_distance_minutes = int(
                time_distance.total_seconds() / 60)  # 시간 간격을 분 단위로 계산
            return time_distance_minutes

        return 0

    class Meta:
        model = TaskLog
        fields = '__all__'


class TaskSerializerForToday(serializers.ModelSerializer):
    task_manager = UserProfileImageSerializer()

    class Meta:
        model = ProjectProgress
        fields = [
            "id",
            "task",
            "in_progress",
            "is_testing",
            "order",
            "task_manager",
            "task_completed",
            "current_status",
            "is_urgent_request",
            "is_task_for_cash_prize",
            "due_date",
        ]


class TestersForTestSerializer(serializers.ModelSerializer):
    tester = UserProfileImageSerializer()  # 필요한 경우 태스크 정보를 시리얼화

    class Meta:
        model = TestersForTest
        fields = (
            "pk",
            "test",
            "tester"
        )


class TestersForTestForExtraTaskSerializer(serializers.ModelSerializer):
    tester = UserProfileImageSerializer()  # 필요한 경우 태스크 정보를 시리얼화

    class Meta:
        model = TestersForTestForExtraTask
        fields = (
            "pk",
            "test",
            "tester"
        )


class CreateTestSerializerForOneTask(ModelSerializer):

    class Meta:
        model = TestForTask
        fields = (
            "test_description",
            "test_method",
            "test_passed"
        )


class CreateCommentSerializerForTask(ModelSerializer):

    class Meta:
        model = TaskComment
        fields = (
            "task",
            "comment",
        )


class CreateExtraTaskSerializer(serializers.ModelSerializer):
    # task_manager = TinyUserSerializer(read_only=True)

    class Meta:
        model = ExtraTask
        fields = (
            "pk",
            "original_task",
            "task_manager",
            "task",
            "importance",
        )

# 0602 refer


class TestSerializerForOneTask(ModelSerializer):
    testers_for_test = TestersForTestSerializer(many=True)
    test_result_images = TestResultImageForTaskSerializer(many=True)

    class Meta:
        model = TestForTask
        fields = (
            "pk",
            "test_description",
            "test_passed",
            "test_method",
            "test_result_image",
            "testers_for_test",
            "test_result_images"
        )


class CreateTestSerializerForExtraTask(ModelSerializer):
    class Meta:
        model = TestForExtraTask
        fields = (
            "test_description",
            "test_method",
            "test_passed"
        )


class TestSerializerForExtraTask(ModelSerializer):
    testers_for_test = TestersForTestForExtraTaskSerializer(many=True)
    test_result_images = TestResultImageForExtraTaskSerializer(many=True)

    class Meta:
        model = TestForExtraTask
        fields = (
            "pk",
            "test_description",
            "test_passed",
            "test_method",
            "test_result_image",
            "testers_for_test",
            "test_result_images"
        )


class ExtraTasksSerializer(ModelSerializer):
    task_manager = UserProfileImageSerializer()
    started_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ExtraTask
        fields = (
            "pk",
            "task_manager",
            "task",
            "task_url1",
            "task_url2",
            "task_status",
            "importance",
            "started_at",
            "completed_at",
            "started_at_formatted"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()


class TaskCommentSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    writer = UserProfileImageSerializer()

    class Meta:
        model = TaskComment
        fields = (
            'id',
            'task',
            'writer',
            'comment',
            'is_edit_mode',
            'like_count',
            'created_at',
            "created_at_formatted"
        )
        read_only_fields = ('id', 'created_at',)

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()

# http://127.0.0.1:8000/api/v1/project_progress/getTaskListForTaskIntegration


class SerializerForTaskListForSelectTargetForIntergration(serializers.ModelSerializer):
    task_manager = UserProfileImageSerializer()
    is_for_today = serializers.SerializerMethodField()
    extra_tasks = ExtraTasksSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "id",
            "task_manager",
            "writer",
            "task",
            "task_manager",
            "current_status",
            "is_for_today",
            "extra_tasks",
        )

    def get_is_for_today(self, obj):
        # 현재 시간을 현지 시간으로 설정
        local_time = timezone.localtime(timezone.now()).date()

        # obj.due_date를 현지 시간으로 변환하여 오늘과 비교
        return obj.due_date.date() == local_time


class ProjectProgressDetailSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    task_images = ReferImageForTaskSerializer(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    tests_for_task = TestSerializerForOneTask(many=True)
    task_comments = TaskCommentSerializer(many=True)
    task_manager = UserProfileImageSerializer()
    task_urls = TaskUrlForTaskSerializer(many=True)
    time_left_to_due_date = serializers.SerializerMethodField()

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "task_urls",
            "task_description",
            "task_url1",
            "task_url2",
            "writer",
            "task_manager",
            "importance",
            "task_completed",
            "started_at",
            "started_at_formatted",
            "due_date",
            "time_left_to_due_date",
            "elapsed_time_from_started_at",
            "task_images",
            "task_comments",
            "extra_tasks",
            "tests_for_task",
            "cash_prize",
            "is_urgent_request",
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def get_time_left_to_due_date(self, obj):
        return obj.time_left_to_due_date()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()


class ChallegersForCachPrizeSerializer(serializers.ModelSerializer):

    challenger = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = ChallengersForCashPrize
        fields = (
            "pk",
            "task",
            "challenger"
        )


class UncompletedTaskSerializerForCashPrize(serializers.ModelSerializer):
    challegers_for_cach_prize = ChallegersForCachPrizeSerializer(many=True)
    task_manager = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "task_manager",
            "writer",
            "current_status",
            "is_task_for_cash_prize",
            "task_completed",
            "current_status",
            "challegers_for_cach_prize",
            "cash_prize",
            "check_for_cash_prize"
        )

# 0612 fix


class SerializerForUncompletedTaskDetailListForChecked(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    completed_at_formatted = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    time_consumed_from_start_to_complete = serializers.SerializerMethodField()
    time_left_to_due_date = serializers.SerializerMethodField()
    task_manager = TinyUserSerializer(read_only=True)
    task_urls = TaskUrlForTaskSerializer(many=True)
    task_comments = ExtraTaskCommentSerializer(many=True)
    tests_for_task = TestSerializerForOneTask(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    task_images = ReferImageForTaskSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "id",
            "writer",
            "task",
            "task_description",
            "task_urls",
            "task_comments",
            "tests_for_task",
            "extra_tasks",
            "task_manager",
            "importance",
            "is_testing",
            "in_progress",
            "task_completed",
            "current_status",
            "due_date",
            "task_classification",
            "started_at",
            "started_at_formatted",
            "completed_at_formatted",
            "due_date_formatted",
            "elapsed_time_from_started_at",
            "time_consumed_from_start_to_complete",
            "time_left_to_due_date",
            "check_result_by_tester",
            "score_by_tester",
            "is_task_for_cash_prize",
            "is_task_for_urgent",
            "cash_prize",
            "task_images"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def completed_at_formatted(self, obj):
        return obj.completed_at_formatted()

    def get_due_date_formatted(self, obj):
        return obj.due_date_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()

    def get_time_consumed_from_start_to_complete(self, obj):
        return obj.time_consumed_from_start_to_complete()

    def get_time_left_to_due_date(self, obj):
        return obj.time_left_to_due_date()

# fix 0705


class SerializerForExtraManager(serializers.ModelSerializer):
    task_manager = UserProfileImageSerializer()

    class Meta:
        model = ExtraTask
        fields = [
            'id',
            'task_manager',
            'original_task'
        ]

class ProjectProgressListSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    completed_at_formatted = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    time_left_to_due_date = serializers.SerializerMethodField()
    task_manager = UserProfileImageSerializer()
    task_images = ReferImageForTaskSerializer(many=True)
    is_for_today = serializers.SerializerMethodField()
    is_due_date_has_passed = serializers.SerializerMethodField()
    d_day_count = serializers.SerializerMethodField()
    extra_managers = SerializerForExtraManager(many=True)
    count_for_extra_tasks = serializers.SerializerMethodField()
    count_for_tests_for_task = serializers.SerializerMethodField()
    count_for_task_comments = serializers.SerializerMethodField()
    count_for_task_images = serializers.SerializerMethodField()
    # task_comments = ExtraTaskCommentSerializer(many=True)
    # test_result_images = TestResultImageForCompletedTaskSerializer(many=True)
    # time_consumed_from_start_to_complete = serializers.SerializerMethodField()

    class Meta:
        model = ProjectProgress
        fields = (
            "id",
            "writer",
            'extra_managers',
            "task",
            "task_images",
            "task_description",
            "task_manager",
            "importance",
            "task_classification",
            "is_testing",
            "in_progress",
            "task_completed",
            "current_status",
            'is_for_today',
            'd_day_count',
            'is_due_date_has_passed',
            "started_at",
            "started_at_formatted",
            "due_date",
            'due_date_option_for_today',
            "due_date_formatted",
            "elapsed_time_from_started_at",
            "completed_at_formatted",
            "time_left_to_due_date",
            "is_task_for_cash_prize",
            "is_task_for_urgent",
            "count_for_task_images",
            "count_for_extra_tasks",
            "count_for_tests_for_task",
            "count_for_task_comments"
            # "time_consumed_from_start_to_complete",
            # 'task_comments',
            # 'test_result_images',
            # "check_result_by_tester",
            # "cash_prize",
            # "score_by_tester",
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def completed_at_formatted(self, obj):
        return obj.completed_at_formatted()

    def get_due_date_formatted(self, obj):
        return obj.due_date_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()

    def get_time_consumed_from_start_to_complete(self, obj):
        return obj.time_consumed_from_start_to_complete()

    def get_time_left_to_due_date(self, obj):
        return obj.time_left_to_due_date()

    def get_is_for_today(self, obj):
        # 현재 시간을 현지 시간으로 설정
        local_time = timezone.localtime(timezone.now()).date()

        # obj.due_date를 현지 시간으로 변환하여 오늘과 비교
        return obj.due_date.date() == local_time

    def get_is_due_date_has_passed(self, obj):
        # 현재 시간을 현지 시간으로 설정
        local_time = timezone.localtime(timezone.now())

        # obj.due_date를 현지 시간으로 변환하여 현재 시간과 비교
        obj_local_time = timezone.localtime(obj.due_date)
        is_due_date_has_passed = obj_local_time < local_time
        return is_due_date_has_passed

    def get_d_day_count(self, obj):
        # 현재 시간을 현지 시간으로 설정
        local_time = timezone.localtime(timezone.now())
        print("local_time : ", local_time)

        # obj.due_date를 현지 시간으로 변환하여 현재 시간과 비교
        obj_local_time = timezone.localtime(obj.due_date)
        print("obj_local_time : ", obj_local_time)

        if obj_local_time > local_time:
            # D-day까지 남은 일 수 계산
            d_day = obj_local_time - local_time
            return f"- {d_day.days}일"
        else:
            # 이미 D-day가 지났거나 오늘인 경우
            over_time = local_time - obj_local_time
            over_time_seconds = int(over_time.total_seconds())  # 초로 변환
            # 일, 시간, 분 계산
            days = over_time_seconds // (24 * 3600)
            hours = (over_time_seconds % (24 * 3600)) // 3600
            minutes = (over_time_seconds % 3600) // 60

            # 결과 반환
            return f"+ {days}일 {hours}시간 {minutes}분"

    def get_count_for_extra_tasks(self, obj):
        countForExtraTaks = obj.extra_tasks.count()
        return countForExtraTaks
    
    def get_count_for_tests_for_task(self, obj):
        countForTest = obj.tests_for_task.count()
        return countForTest
    
    def get_count_for_task_comments(self, obj):
        countForComments = obj.task_comments.count()
        return countForComments
    def get_count_for_task_images(self, obj):
        countForTaskImages = obj.task_images.count()
        return countForTaskImages



def get_current_time_in_seoul():
    seoul_tz = pytz.timezone('Asia/Seoul')
    return datetime.now(seoul_tz)


def get_due_date_mapping_value(value):
    now_in_seoul = get_current_time_in_seoul()
    due_date_mapping = {
        'morning_tasks': now_in_seoul.replace(hour=12, minute=59),
        'afternoon_tasks': now_in_seoul.replace(hour=18, minute=59),
        'night_tasks': now_in_seoul.replace(hour=23, minute=59),
        'tomorrow': now_in_seoul.replace(hour=18, minute=59) + timedelta(days=1),
        'day-after-tomorrow': now_in_seoul.replace(hour=18, minute=59) + timedelta(days=2),
        'this-week': now_in_seoul.replace(hour=18, minute=59) + timedelta(days=7 - now_in_seoul.weekday()),
        'this-month': now_in_seoul.replace(day=1, hour=18, minute=59) + timedelta(days=32 - now_in_seoul.day),
    }
    return due_date_mapping.get(value, None)


class CreateProjectProgressSerializer(serializers.ModelSerializer):

    task_manager = TinyUserSerializer(read_only=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "writer",
            "task_manager",
            "importance",
            "task_completed",
            "task_classification",
            "due_date"
        )

    def to_internal_value(self, data):
        due_date_option = data.get('due_date_option')
        if due_date_option:
            due_date = get_due_date_mapping_value(due_date_option)
            if due_date is not None:
                data['due_date'] = due_date

        return super().to_internal_value(data)


class TargetTaskSerializer(serializers.ModelSerializer):
    task_images = ReferImageForTaskSerializer(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    task_manager = UserProfileImageSerializer()
    # tests_for_tasks = TestSerializerForOneTask(many=True)
    # task_comments = TaskCommentSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "id",
            "task",
            "task_manager",
            "importance",
            "task_completed",
            "task_images",
            "due_date",
            "extra_tasks",
        )
