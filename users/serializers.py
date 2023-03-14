from medias.serializers import ProfilePhotoSerializer
from rest_framework.serializers import ModelSerializer
from .models import SkillForFrameWork, User, UserPosition


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
        

class UserPostionSerializer(ModelSerializer):
    class Meta:
        model = UserPosition
        fields = (
            "pk",
            "position_name",
        )


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
    position = UserPostionSerializer()

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
        )


class UserListSerializer(ModelSerializer):
    profileImages = ProfilePhotoSerializer(many=True)

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
            # "name",
            "username",
            # "profile_image",
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
