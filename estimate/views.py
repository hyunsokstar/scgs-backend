from django.shortcuts import render
# from requests import Response
from rest_framework.response import Response

from rest_framework.views import APIView
from .models import Estimate
from estimate.serializers import EstimateRequireSerializer

# Create your views here.


class Estimates(APIView):
    def get(self, request):
        all_estimate_requires = Estimate.objects.all()
        print("견적 요청 리스트 : ", all_estimate_requires)

        serializer = EstimateRequireSerializer(
            all_estimate_requires, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EstimateRequireSerializer(data=request.data)
        if serializer.is_valid():
            estimate_require = serializer.save()
            return Response(EstimateRequireSerializer(estimate_require).data)
        else:
            return Response(serializer.errors)