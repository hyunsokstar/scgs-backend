from rest_framework import serializers
from .models import Survey, SurveyOption
from users.serializers import UserProfileImageSerializer

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ('id', 'content', 'survey')

# 시리얼라이저 수정
class SurveyDetailSerializer(serializers.ModelSerializer):
    survey_options = SurveyOptionSerializer(many=True, read_only=True)
    writer = UserProfileImageSerializer(read_only=True)
    
    # 추가된 필드
    count_for_1th_option = serializers.SerializerMethodField()
    count_for_2th_option = serializers.SerializerMethodField()
    count_for_3th_option = serializers.SerializerMethodField()
    count_for_4th_option = serializers.SerializerMethodField()
    count_for_5th_option = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('id', 'writer', 'title', 'survey_options', 'created_at',
                  'count_for_1th_option', 'count_for_2th_option',
                  'count_for_3th_option', 'count_for_4th_option',
                  'count_for_5th_option')

    # 각 옵션별 응답 개수 계산 메서드
    def get_count_for_1th_option(self, obj):
        return obj.survey_answers.filter(selected_option__id=1).count()

    def get_count_for_2th_option(self, obj):
        return obj.survey_answers.filter(selected_option__id=2).count()

    def get_count_for_3th_option(self, obj):
        return obj.survey_answers.filter(selected_option__id=3).count()

    def get_count_for_4th_option(self, obj):
        return obj.survey_answers.filter(selected_option__id=4).count()

    def get_count_for_5th_option(self, obj):
        return obj.survey_answers.filter(selected_option__id=5).count()


class SurveySerializer(serializers.ModelSerializer):
    survey_options = SurveyOptionSerializer(many=True, read_only=True)
    writer = UserProfileImageSerializer(read_only=True)


    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'writer', 'survey_options', 'created_at')