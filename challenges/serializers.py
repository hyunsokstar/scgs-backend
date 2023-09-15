from rest_framework import serializers
from .models import Challenge
from users.serializers import UserProfileImageSerializer

class SerializerForChallenges(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)  # UserProfileImageSerializer는 다른 곳에서 정의되어 있어야 합니다.
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = (
            'id',
            'title',
            'subtitle',
            'description',
            'main_image',
            'writer',
            'created_at',
            'created_at_formatted',
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%y년 %m월 %d일')
