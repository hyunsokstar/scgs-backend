from users.serializers import UserNameSerializer
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
            "elapsed_time_from_started_at"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()


class ProjectProgressListSerializer(serializers.ModelSerializer):

    started_at_formatted = serializers.SerializerMethodField()
    elapsed_time_from_started_at = serializers.SerializerMethodField()

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
            "elapsed_time_from_started_at"
        )

    def get_started_at_formatted(self, obj):
        return obj.started_at_formatted()

    def get_elapsed_time_from_started_at(self, obj):
        return obj.elapsed_time_from_started_at()


class CreateProjectProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProgress
        fields = (
            "pk",
            "task",
            "writer",
            "importance",
            "task_completed",
        )

    # def save(self, **kwargs):
    #     self.validated_data['started_at'] = timezone.localtime(timezone.now())
    #     return super().save(**kwargs)
