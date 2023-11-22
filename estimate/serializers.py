from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from .models import Estimate
from rest_framework import serializers


# Create your views here.


# title,
# product,
# manager,
# email,
# phone_number,
# content
# estimate_require_completion
# memo

class EstimateRequireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = (
            "pk",
            "title",
            "product",
            "manager",
            "email",
            "phone_number",
            "content",
            "estimate_require_completion",
            "memo",
        )
        optional_fields = ['title', 'product','manager','email',"phone_number", "content", "estimate_require_completion", "memo"]


