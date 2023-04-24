from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import StudyNote

class StudyNoteSerializer(serializers.ModelSerializer):

    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNote
        fields = ['pk', 'title', 'description', 'writer']