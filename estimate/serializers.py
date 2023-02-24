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

    # title = serializers.CharField(required=False)
    # product = serializers.CharField(required=False)
    # manager = serializers.CharField(required=False)
    # email = serializers.CharField(required=False)
    # phone_number = serializers.CharField(required=False)
    # content = serializers.CharField(required=False)
    # estimate_require_completion = serializers.CharField(required=False)
    # memo = serializers.CharField(required=False)

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
        # extra_kwargs = {'pk':{'required':False},'title': {'required': False}, 'product': {'required': False}, 
        #                 'manager': {'required': False}, 'email': {'required': False}, 
        #                 'phone_number': {'required': False}, 'content': {'required': False},
        #                 'estimate_require_completion': {'required': False}, 
        #                 'memo': {'required': False}
        #                 }

