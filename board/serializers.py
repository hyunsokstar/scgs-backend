from rest_framework import serializers
from django.utils import timezone

from .models import (
    Suggestion,
    CommentForSuggestion,
)
from users.serializers import UserProfileImageSerializer

# SerializerForCreateSuggestionForBoard
class SerializerForCommentListForSuggestionForBoard(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = CommentForSuggestion
        fields = ['id', 'writer', 'content', 'created_at']


class SerializerForCreateSuggestionForBoard(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['title', 'content', 'writer']

class SuggestionSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Suggestion
        fields = (
            'id',
            'title',
            'content',
            'writer',
            # 'created_at',
            # 'updated_at',
            'created_at_formatted',
            'updated_at_formatted'
        )

    def get_created_at_formatted(self, obj):
        local_created_at = timezone.localtime(obj.created_at)
        return local_created_at.strftime('%y년 %m월 %d일 %H시 %M분')

    def get_updated_at_formatted(self, obj):
        local_updated_at = timezone.localtime(obj.updated_at)
        return local_updated_at.strftime('%y년 %m월 %d일 %H시 %M분')
