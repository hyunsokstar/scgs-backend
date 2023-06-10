from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import StudyNote, StudyNoteContent


# class StudyNoteSerializer(serializers.ModelSerializer):
#     writer = UserProfileImageSerializer(read_only=True)

#     class Meta:
#         model = StudyNote
#         fields = ['pk', 'title', 'description', 'writer']
class StudyNoteSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)
    count_for_note_contents = serializers.SerializerMethodField()

    class Meta:
        model = StudyNote
        fields = ['pk', 'title', 'description',
                  'writer', 'count_for_note_contents']

    def get_count_for_note_contents(self, obj):
        return obj.note_contents.count()


class StudyNoteContentSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = StudyNoteContent
        fields = ['pk', 'title', 'file_name', 'content',
                  'writer', 'created_at', 'page', 'order']
        read_only_fields = ['id', 'created_at']
