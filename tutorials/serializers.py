from users.serializers import TinyUserSerializer
from .models import Tutorial
from rest_framework import serializers
from requests import Response


class TutorialListSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(read_only=True)

    class Meta:
        model = Tutorial
        fields = (
            "pk",
            "author",
            "tutorial_image",
            "title",
            "teacher",
            "price",
            "description",
            "frontend_framework_option",
            "backend_framework_option",
            "tutorial_url",
            'like_count',
            "unlike_count"
        )


class TutorialDetaailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = (
            "pk",
            "tutorial_image",
            "title",
            "teacher",
            "price",
            "description",
            "frontend_framework_option",
            "backend_framework_option",
            "tutorial_url",
        )

class TutorialDetaailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = (
            "pk",
            "tutorial_image",
            "title",
            "teacher",
            "price",
            "description",
            "frontend_framework_option",
            "backend_framework_option",
            "tutorial_url",
        )
