from rest_framework.serializers import ModelSerializer
from .models import (
    Photo,
    PhotoForProfile,
    ReferImageForTask,
    TestResultImageForTask,
    TestResultImageForExtraTask,
    ReferImageForExtraTask,
    TestResultImageForCompletedTask
)


class TestResultImageForCompletedTaskSerializer(ModelSerializer):
    class Meta:
        model = TestResultImageForCompletedTask
        fields = (
            "pk",
            "image_url",
        )


class TestResultImageForTaskSerializer(ModelSerializer):
    class Meta:
        model = TestResultImageForTask
        fields = (
            "pk",
            "image_url"
        )


class TestResultImageForExtraTaskSerializer(ModelSerializer):
    class Meta:
        model = TestResultImageForExtraTask
        fields = (
            "pk",
            "image_url"
        )


class ProfilePhotoSerializer(ModelSerializer):
    class Meta:
        model = PhotoForProfile
        fields = (
            "pk",
            "file",
        )


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )


class ReferImageForTaskSerializer(ModelSerializer):
    class Meta:
        model = ReferImageForTask
        fields = (
            "pk",
            "image_url",
            # "task",
        )


class ReferImageForExtraTaskSerializer(ModelSerializer):
    class Meta:
        model = ReferImageForExtraTask
        fields = (
            "pk",
            "image_url",
            # "task",
        )


class TestResultImageSerializer(ModelSerializer):
    class Meta:
        model = TestResultImageForTask
        fields = (
            "pk",
            "image_url",
        )
