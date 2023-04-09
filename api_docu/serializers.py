from rest_framework import serializers
from .models import ApiDocu

class ApiDocuSerializer(serializers.ModelSerializer):
    classification = serializers.CharField(source='get_classification_display')

    class Meta:
        model = ApiDocu
        fields = (
            'id',
            'classification',
            'url',
            'description',
        )