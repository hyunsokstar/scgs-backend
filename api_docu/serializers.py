from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import ApiDocu

class ApiDocuSerializer(serializers.ModelSerializer):
    classification = serializers.CharField(source='get_classification_display')
    writer = UserProfileImageSerializer()

    class Meta:
        model = ApiDocu
        fields = (
            'id',
            'url',
            'description',
            'classification',
            'writer',
        )

class SerializerForInsertToApiDocu(serializers.ModelSerializer):

    class Meta:
        model = ApiDocu
        fields = (
            'url',
            'description',
            'classification',
            'writer',
        )    