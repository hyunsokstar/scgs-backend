from medias.serializers import ProfilePhotoSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import SkillForFrameWork, User, UserPosition, UserTaskComment
from project_progress.models import ProjectProgress
from django.utils import timezone
from datetime import datetime, time


class UserProfileImageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "profile_image"
        )


class UsersForCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username"
        )


class UserNameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "admin_level",
            "position",
        )


class UserPositionSerializer(ModelSerializer):
    class Meta:
        model = UserPosition
        fields = (
            "pk",
            "position_name"
        )


class AddMultiUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "email",
            "admin_level",
            "position",
        )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('이미 존재하는 username입니다.')
        return value


class SkillForFrameWorkSerializer(ModelSerializer):
    class Meta:
        model = SkillForFrameWork
        fields = (
            "pk",
            "frame_work_name",
        )


class UserProfileSerializer(ModelSerializer):
    profileImages = ProfilePhotoSerializer(many=True)
    skill_for_frameWork = SkillForFrameWorkSerializer(many=True)
    position = UserPositionSerializer()

    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "username",
            "email",
            "profileImages",
            'position',
            "skill_for_frameWork",
            'about_me',
            'admin_level',
            'profile_image',
            'is_edit_mode_for_study_note_contents',
            'study_note_url1',
            'study_note_url2'
        )


class UserListSerializer(ModelSerializer):
    profileImages = ProfilePhotoSerializer(many=True)
    position = UserPositionSerializer()

    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "username",
            "email",
            "profileImages",
            "admin_level",
            "position"
        )


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username"
        )


class PrivateUserSerializer(ModelSerializer):
    # profileImages = ProfilePhotoSerializer(many=True)

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            # "profileImages",
        )

class TaskCommentSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer()

    class Meta:
        model = UserTaskComment
        fields = (
            'id',
            'writer',
            'comment',
            'like_count',
            'created_at',
            'created_at_formatted'
        )
        read_only_fields = ('id', 'created_at')

    def get_created_at_formatted(self, obj):
        return obj.created_at_formatted()

class TaskStatusForTeamMembersSerializer(serializers.ModelSerializer):
    position = serializers.StringRelatedField()
    total_count_for_task = serializers.SerializerMethodField()
    completed_count_for_task = serializers.SerializerMethodField()
    uncompleted_count_for_task = serializers.SerializerMethodField()
    total_count_for_task_for_today = serializers.SerializerMethodField()
    count_for_uncompleted_task_for_today = serializers.SerializerMethodField()
    count_for_completed_task_for_today = serializers.SerializerMethodField()
    user_task_comments = TaskCommentSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'profile_image',
            'position',
            'cash',
            'total_count_for_task',
            'uncompleted_count_for_task',
            'completed_count_for_task',
            'total_count_for_task_for_today',
            'count_for_uncompleted_task_for_today',
            'count_for_completed_task_for_today',
            'task_in_progress',
            'user_task_comments'
        ]

    def get_total_count_for_task(self, obj):
        return ProjectProgress.objects.filter(task_manager=obj).count()

    def get_completed_count_for_task(self, obj):
        return ProjectProgress.objects.filter(task_manager=obj, current_status=ProjectProgress.TaskStatusChoices.completed).count()

    def get_uncompleted_count_for_task(self, obj):
        return ProjectProgress.objects.filter(task_manager=obj).exclude(current_status=ProjectProgress.TaskStatusChoices.completed).count()

    def get_total_count_for_task_for_today(self, obj):
        today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.localtime().replace(hour=23, minute=59, second=59, microsecond=999999)
        return ProjectProgress.objects.filter(task_manager=obj, due_date__range=(today_start, today_end)).count()

    def get_count_for_completed_task_for_today(self, obj):
        today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.localtime().replace(hour=23, minute=59, second=59, microsecond=999999)
        return ProjectProgress.objects.filter(task_manager=obj, due_date__range=(today_start, today_end), current_status=ProjectProgress.TaskStatusChoices.completed).count()

    def get_count_for_uncompleted_task_for_today(self, obj):
        today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = timezone.localtime().replace(hour=23, minute=59, second=59, microsecond=999999)
        return ProjectProgress.objects.filter(task_manager=obj, due_date__range=(today_start, today_end)).exclude(current_status=ProjectProgress.TaskStatusChoices.completed).count()
    
class SerializerForCreateForUserTaskComment(ModelSerializer):

    class Meta:
        model = UserTaskComment
        fields = (
            "owner",
            "comment",
        )
