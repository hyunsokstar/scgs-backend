from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import ShortCut, Tags, RelatedShortcut, ShortCutHub, ShortCutHubContent


class ShortcutHubSerializer(serializers.ModelSerializer):
    writer = UserProfileImageSerializer()
    total_count_for_shortcut_hub_contents = serializers.SerializerMethodField()

    class Meta:
        model = ShortCutHub
        fields = (
            "id",
            "title",
            "description",
            "writer",
            "total_count_for_shortcut_hub_contents",
            "created_at",
        )

    def get_total_count_for_shortcut_hub_contents(self, obj):
        return obj.contents.count()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("id", "name")


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
            "id",
            "writer",
            # 'shortcut',
            "description",
            "classification",
            "tags",
            "related_shortcut_count",  # Add this line
        )

    def get_related_shortcut_count(self, obj):
        return RelatedShortcut.objects.filter(shortcut=obj).count()


class ShortCutHubContentSerializer(serializers.ModelSerializer):
    shortcut = ShortCutSerializer()

    class Meta:
        model = ShortCutHubContent
        fields = ["id", "shortcut", "shortcut_hub", "writer", "order", "created_at"]


class RelatedShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedShortcut
        fields = "__all__"


class SerializerForInsertToShortcut(serializers.ModelSerializer):
    class Meta:
        model = ShortCut
        fields = (
            "description",
            "classification",
        )
