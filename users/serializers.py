from medias.serializers import ProfilePhotoSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import SkillForFrameWork, User, UserPosition
from project_progress.models import ProjectProgress
from django.utils import timezone


class TaskStatusForTeamMembersSerializer(serializers.ModelSerializer):
    position = serializers.StringRelatedField()
    total_count_for_task = serializers.SerializerMethodField()
    completed_count_for_task = serializers.SerializerMethodField()
    uncompleted_count_for_task = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'profile_image',
            'position',
            'cash',
            'total_count_for_task',
            'uncompleted_count_for_task',
            'completed_count_for_task',
            'task_in_progress'
        ]

    def get_total_count_for_task(self, obj):
        return ProjectProgress.objects.filter(task_manager=obj).count()

    def get_completed_count_for_task(self, obj):
        end_of_today = timezone.now().replace(hour=23, minute=59, second=59)
        return ProjectProgress.objects.filter(task_manager=obj, completed_at__lte=end_of_today, current_status=ProjectProgress.TaskStatusChoices.completed).count()

    def get_uncompleted_count_for_task(self, obj):
        end_of_today = timezone.now().replace(hour=23, minute=59, second=59)
        return ProjectProgress.objects.filter(task_manager=obj, due_date__lte=end_of_today).exclude(current_status=ProjectProgress.TaskStatusChoices.completed).count()


# class TaskStatusForTeamMembersSerializer(serializers.ModelSerializer):
#     position = serializers.StringRelatedField()

#     class Meta:
#         model = User
#         fields = ['username', 'position']

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
            'is_edit_mode_for_study_note_contents'
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
