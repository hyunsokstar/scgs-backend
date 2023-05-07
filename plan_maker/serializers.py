from rest_framework import serializers
from .models import LongTermPlan


class LongTermPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermPlan
        fields = '__all__'