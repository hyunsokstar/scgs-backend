from users.serializers import UserProfileImageSerializer
from rest_framework import serializers
from .models import LongTermPlan, LongTermPlanContents


class LongTermPlanContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermPlanContents
        fields = ['id',
                  'long_term_plan',
                  'start',
                  'end',
                  'name',
                  'progress',
                  'displayOrder',
                  'dependencies'
                  ]


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
