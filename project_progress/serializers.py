# from medias.serializers import ReferImageForTaskSerializer, TestResultImageForTaskSerializer,TestResultImageForExtraTaskSerializer, ReferImageForExtraTaskSerializer
from medias.serializers import (
    ReferImageForTaskSerializer,
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

from rest_framework import serializers
from requests import Response
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from datetime import timedelta, datetime
import pytz

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
    testers_for_test_for_extra_task = TestersForTestForExtraTaskSerializer(many=True)
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

# 1122 0611
class ProjectProgressDetailSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    task_images = ReferImageForTaskSerializer(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    tests_for_tasks = TestSerializerForOneTask(many=True)
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
            "tests_for_tasks",
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
    tests_for_tasks = TestSerializerForOneTask(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    task_images = ReferImageForTaskSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "writer",
            "task",
            "task_description",
            "task_urls",
            "task_comments",
            "tests_for_tasks",
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

# fix 0607
class ProjectProgressListSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    completed_at_formatted = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    time_consumed_from_start_to_complete = serializers.SerializerMethodField()
    time_left_to_due_date = serializers.SerializerMethodField()
    task_manager = UserProfileImageSerializer()
    # task_urls = TaskUrlForTaskSerializer(many=True)
    # challegers_for_cach_prize = ChallegersForCachPrizeSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "writer",
            "task",
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
            # "task_urls"
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
