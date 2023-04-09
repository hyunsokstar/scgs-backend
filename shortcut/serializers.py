from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import ShortCut

class ShortCutSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer()

    class Meta:
        model = ShortCut
        fields = (
            'id',
            'writer',
            'shortcut',
            'description',
            'classification',
        )