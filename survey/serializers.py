from rest_framework import serializers
from .models import Survey, SurveyOption

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ('id', 'content', 'survey')

class SurveySerializer(serializers.ModelSerializer):
    survey_options = SurveyOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'writer', 'survey_options')