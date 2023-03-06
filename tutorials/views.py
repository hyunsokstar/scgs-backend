# from http.client import NOT_FOUND
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Tutorial
from rest_framework.response import Response
from tutorials.serializers import TutorialDetaailSerializer, TutorialListSerializer

from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK


class Tutorials(APIView):
    def get(self, request):
        all_tutorials = Tutorial.objects.all()
        print("count : ", all_tutorials.count())
        serializer = TutorialListSerializer(all_tutorials, many=True)
        print("serializer length: ", serializer)
        return Response(serializer.data)

    def post(self, request):
        print("tutorial posting check")
        serializer = TutorialListSerializer(data=request.data)
        if serializer.is_valid():
            tutorial = serializer.save()
            return Response(TutorialListSerializer(tutorial).data)
        else:
            print("serializer is not valid : ", serializer.errors)
            return Response(serializer.errors)


# tutorial update view
class TutorialDetail(APIView):

    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        print("TutorialDetail view 요청 확인 !!")
        print(pk, type(pk))
        tutorial = self.get_object(pk)
        # print("Tutorial : ", Tutorial)
        serializer = TutorialDetaailSerializer(
            tutorial, context={"request": request}
        )
        print("/Tutorials/:pk 에 대해 클라이언트로 넘너가는 데이터 serializer.data: ", serializer.data)
        return Response(serializer.data)

    def put(self, request, pk):
        print("request.data", request.data)
        print("pk : ", pk)

        tutorial = self.get_object(pk)
        serializer = TutorialDetaailSerializer(
                tutorial,
                data=request.data,
                partial=True
            )
            
        if serializer.is_valid():
            tutorial = self.get_object(pk)
            print("serializer 유효함")
            try:
                tutorial = serializer.save()
                serializer = TutorialDetaailSerializer(tutorial)
                return Response(serializer.data)

            except Exception as e:
                print("ee : ", e)
                raise ParseError("tutorial not found")
        else:
            print("시리얼 라이저가 유효하지 않음")
            raise ParseError("serializer is not valid")
        
    def delete(self, request, pk):
        print("삭제 요청 확인")
        tutorial = self.get_object(pk)
        tutorial.delete()
        return Response(status=HTTP_204_NO_CONTENT)  