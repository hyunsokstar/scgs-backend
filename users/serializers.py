from rest_framework.serializers import ModelSerializer
from .models import User

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
            "is_host",
            "gender",
            "language",
        )

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            # "username",
        )

class PrivateUserSerializer(ModelSerializer):
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
        )