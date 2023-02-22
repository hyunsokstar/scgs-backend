from django.shortcuts import render
# from requests import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
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


class EstimateDetail(APIView):
    def get_object(self, pk):
        try:
            return Estimate.objects.get(pk=pk)
        except Estimate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        print("견적 디테일 페이지 요청 확인 (백엔드) !")
        print(pk, type(pk))
        estimate = self.get_object(pk)
        print("estimate : ", estimate)

        serializer = EstimateRequireSerializer(estimate, context={"request":request})  

        return Response(serializer.data)