from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import ShortCut, Tags


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


class ShortCutSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = ShortCut
        fields = (
            'id',
            'writer',
            'shortcut',
            'description',
            'classification',
            'tags'
        )


class SerializerForInsertToShortcut(serializers.ModelSerializer):
    class Meta:
        model = ShortCut
        fields = (
            'shortcut',
            'description',
            'classification',
            # 'tags'
        )
