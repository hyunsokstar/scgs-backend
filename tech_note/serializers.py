from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import TechNote, TechNoteContent


class TechNoteSerializer(serializers.ModelSerializer):
    note_content_count = serializers.SerializerMethodField()
    author = UserProfileImageSerializer()

    # content_count 가져오기
    class Meta:
        model = TechNote
        fields = (
            'pk',
            'task',
            'author',
            'title',
            'note_content_count',
            'category',
            'like_count',
            'view_count',
            'created_at'
        )

    def get_note_content_count(self, obj):
        return obj.note_content_count

# tech_note_description
# category_option


class CreateTechNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNote
        fields = ('title', 'category','task')


class TechNoteContentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNoteContent
        fields = (
            "pk",
            "tech_note",
            "note_content_title",
            "note_content_file",
            "note_content_content",
            "created_at"
        )


class SerializerForCreateTechNoteContent(serializers.ModelSerializer):
    class Meta:
        model = TechNoteContent
        fields = (
            "tech_note",
            "note_content_title",
            "note_content_file",
            "note_content_content",
            "created_at"
        )
