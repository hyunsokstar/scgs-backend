from rest_framework import serializers
from .models import TechNote


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
