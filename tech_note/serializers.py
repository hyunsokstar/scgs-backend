from rest_framework import serializers
from .models import TechNote, TechNoteContent


class TechNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNote
        fields = ('pk', 'author', 'title', 'category',
                  'like_count', 'view_count', 'created_at')

# tech_note_description
# category_option


class CreateTechNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNote
        fields = ('title', 'category')


class TechNoteContentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNoteContent
        fields = (
            "pk",
            "tech_note",
            "title",
            "file",
            "content",
            "created_at"
        )
