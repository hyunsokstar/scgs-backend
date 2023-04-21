from medias.serializers import ReferImageForTaskSerializer, TestResultImageForTaskSerializer
from users.serializers import TinyUserSerializer, UserNameSerializer, UserProfileImageSerializer
from .models import ExtraTask, ProjectProgress, TaskComment, TestForTask, TestersForTest
from rest_framework import serializers
from requests import Response
from django.utils import timezone
from rest_framework.serializers import ModelSerializer


class TestersForTestSerializer(serializers.ModelSerializer):
    tester = UserProfileImageSerializer()  # 필요한 경우 태스크 정보를 시리얼화

    class Meta:
        model = TestersForTest
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

# 0407 여기에 추가 해야 함


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


class ExtraTasksSerializer(ModelSerializer):
    task_manager = UserProfileImageSerializer()
    started_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ExtraTask
        fields = (
            "pk",
            "task_manager",
            "task",
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


class ProjectProgressDetailSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    task_images = ReferImageForTaskSerializer(many=True)
    extra_tasks = ExtraTasksSerializer(many=True)
    tests_for_tasks = TestSerializerForOneTask(many=True)
    task_comments = TaskCommentSerializer(many=True)
    task_manager = UserProfileImageSerializer()

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "task_description",
            "writer",
            "task_manager",
            "importance",
            "task_completed",
            "started_at",
            "started_at_formatted",
            "due_date",
            "elapsed_time_from_started_at",
            "task_images",
            "task_comments",
            "extra_tasks",
            "tests_for_tasks",
            "cash_prize",
            "is_urgent_request"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()

    # def get_task_manager(self, project):
    #     request = self.context["request"]
    #     return project.task_manager == request.user


class ProjectProgressListSerializer(serializers.ModelSerializer):
    started_at_formatted = serializers.SerializerMethodField()
    completed_at_formatted = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    time_consumed_from_start_to_complete = serializers.SerializerMethodField()
    time_left_to_due_date = serializers.SerializerMethodField()
    task_manager = TinyUserSerializer(read_only=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "writer",
            "task_manager",
            "importance",
            "in_progress",
            "is_testing",
            "task_completed",
            "current_status",
            "started_at",
            "due_date",
            "started_at_formatted",
            "completed_at_formatted",
            "due_date_formatted",
            "elapsed_time_from_started_at",
            "time_consumed_from_start_to_complete",
            "time_left_to_due_date",
            "check_result_by_tester",
            "score_by_tester",
            "is_task_for_cash_prize",
            "cash_prize"
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
        )
