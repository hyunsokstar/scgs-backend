from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import ShortCut, Tags, RelatedShortcut


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


# class ShortCutSerializer(serializers.ModelSerializer):
#     writer = UserProfileImageSerializer()
#     tags = TagsSerializer(many=True)

#     class Meta:
#         model = ShortCut
#         fields = (
#             'id',
#             'writer',
#             'shortcut',
#             'description',
#             'classification',
#             'tags'
#         )

class ShortCutSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer()
    tags = TagsSerializer(many=True)
    related_shortcut_count = serializers.SerializerMethodField()

    class Meta:
        model = ShortCut
        fields = (
            'id',
            'writer',
            'shortcut',
            'description',
            'classification',
            'tags',
            'related_shortcut_count' # Add this line
        )

    def get_related_shortcut_count(self, obj):
        return RelatedShortcut.objects.filter(shortcut=obj).count()

class RelatedShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedShortcut
        fields = "__all__"

class SerializerForInsertToShortcut(serializers.ModelSerializer):
    class Meta:
        model = ShortCut
        fields = (
            'shortcut',
            'description',
            'classification',
        )
