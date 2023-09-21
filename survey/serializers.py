from rest_framework import serializers
from .models import Survey, SurveyOption
from users.serializers import UserProfileImageSerializer

class SerializerForCreateSurvey(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['title', 'description']

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ('id', 'content', 'survey')

# 시리얼라이저 수정
class SurveyDetailSerializer(serializers.ModelSerializer):
    survey_options = SurveyOptionSerializer(many=True, read_only=True)
    writer = UserProfileImageSerializer(read_only=True)

    # 수정된 필드
    count_for_options = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('id', 'writer', 'title', 'survey_options', 'created_at', 'count_for_options')

    # 각 옵션별 응답 개수 계산 메서드
    def get_count_for_options(self, obj):
        options = obj.survey_options.all()
        option_counts = []

        # 각 옵션에 대한 응답 개수 가져오기
        for option in options:
            count = obj.survey_answers.filter(selected_option=option).count()
            option_counts.append({
                'option_content': option.content,
                'count': count
            })  # 옵션 제목과 응답 개수를 딕셔너리로 추가

        return option_counts





class SurveySerializer(serializers.ModelSerializer):
    survey_options = SurveyOptionSerializer(many=True, read_only=True)
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'writer',
                  'survey_options', 'created_at')
