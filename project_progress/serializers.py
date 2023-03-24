from medias.serializers import ReferImageForTaskSerializer
from users.serializers import TinyUserSerializer, UserNameSerializer
from .models import ProjectProgress
from rest_framework import serializers
from requests import Response
from django.utils import timezone

# task
# writer
# importance
# task_status
# password


class ProjectProgressDetailSerializer(serializers.ModelSerializer):

    started_at_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()
    # writer = UserNameSerializer()
    task_images = ReferImageForTaskSerializer(many=True)

    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "writer",
            "importance",
            "task_completed",
            "started_at",
            "started_at_formatted",
            "due_date",
            "elapsed_time_from_started_at",
            "task_images"
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
            "task_completed",
            "started_at",
            "due_date",
            "started_at_formatted",
            "completed_at_formatted",
            "due_date_formatted",
            "elapsed_time_from_started_at",
            "time_consumed_from_start_to_complete",
            "time_left_to_due_date",
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

    # def save(self, **kwargs):
    #     self.validated_data['started_at'] = timezone.localtime(timezone.now())
    #     return super().save(**kwargs)
