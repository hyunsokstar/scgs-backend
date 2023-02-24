from django.shortcuts import render
# from requests import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Estimate
from estimate.serializers import EstimateRequireSerializer
from rest_framework.status import HTTP_204_NO_CONTENT


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

        serializer = EstimateRequireSerializer(
            estimate, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        print("request.data", request.data)
        print("pk : ", pk)

        estimate = self.get_object(pk)
        serializer = EstimateRequireSerializer(
                estimate,
                data=request.data,
                partial=True
            )
            
        if serializer.is_valid():
            estimate = self.get_object(pk)
            print("serializer 유효함")
            try:
                estimate = serializer.save()
                serializer = EstimateRequireSerializer(estimate)
                return Response(serializer.data)

            except Exception as e:
                print("ee : ", e)
                raise ParseError("Estimate not found")
        else:
            print("시리얼 라이저가 유효하지 않음")
            raise ParseError("serializer is not valid")

            # return Response(serializer.errors)
            
    def delete(self, request, pk):
        print("삭제 요청 확인")
        estimate = self.get_object(pk)
        estimate.delete()
        return Response(status=HTTP_204_NO_CONTENT)            
