from rest_framework import serializers
from .models import TechNote


class TechNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechNote
        fields = ('id', 'author', 'title', 'category',
                  'like_count', 'view_count', 'created_at')
