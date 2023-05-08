from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import LongTermPlan


class LongTermPlanSerializer(serializers.ModelSerializer):

    writer = UserProfileImageSerializer(read_only=True)

    class Meta:
        model = LongTermPlan
        fields = (
            "pk",
            "title",
            "category",
            "description",
            "writer",
            "created_at",
        )
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        writer = self.context['writer']
        validated_data['writer'] = writer
        return super().create(validated_data)        