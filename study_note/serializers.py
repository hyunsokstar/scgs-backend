from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import StudyNote, StudyNoteContent

class StudyNoteSerializer(serializers.ModelSerializer):

    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNote
        fields = ['pk', 'title', 'description', 'writer']

class StudyNoteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyNoteContent
        fields = ['pk', 'title', 'file_name', 'content', 'writer', 'created_at', 'page']
        read_only_fields = ['id', 'created_at']        