import math
from django.shortcuts import render
# from requests import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Estimate
from estimate.serializers import EstimateRequireSerializer
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from django.conf import settings



# Create your views here.

class Estimates(APIView):
    totalCount=0
    
    def get(self, request):
        print("견적 리스트 요청 확인")
        try:
            page = request.query_params.get("page", 1) # query 파라미터에서 page 가져오기 or 1 
            page = int(page)
        except ValueError:
            page = 1        
        
        # 페이지 1일때 0부터 시작 2일때 3부터 시작 3일때 6부터 시작
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size        
        all_estimate_requires = Estimate.objects.all()[start:end]
        
        if(Estimate.objects.all().count()%3 == 0 ):
            self.totalCount = Estimate.objects.all().count()/3
        else:
            self.totalCount = Estimate.objects.all().count()/3 + 1
        
        serializer = EstimateRequireSerializer(all_estimate_requires, many=True)
        
        data = serializer.data
        data = {"totalCount": math.trunc(self.totalCount), "estimateRequires": data}        
        
        # return Response(serializer.data, status = HTTP_200_OK)
        return Response(data, status=HTTP_200_OK)

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
