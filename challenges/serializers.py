from rest_framework import serializers
from .models import (
    Challenge,
    EvaluationCriteria
)
from users.serializers import UserProfileImageSerializer


class SerializerForCreateChallenge(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['title', 'subtitle', 'description', 'main_image', 'writer']


class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = (
            'id',
            'item_description',
            # 다른 EvaluationCriteria 모델의 필드들을 여기에 추가하세요
        )


class SerializerForChallenges(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    created_at_formatted = serializers.SerializerMethodField()
    evaluation_criterials = EvaluationCriteriaSerializer(
        many=True, read_only=True)  # 추가

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
            'evaluation_criterials',  # 추가
        )

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%y년 %m월 %d일')
