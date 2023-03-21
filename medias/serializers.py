from rest_framework.serializers import ModelSerializer
from .models import Photo, PhotoForProfile, ReferImageForTask


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
