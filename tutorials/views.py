# from http.client import NOT_FOUND
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Tutorial
from rest_framework.response import Response
from tutorials.serializers import TutorialDetaailSerializer, TutorialListSerializer

from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK


class TutorialLike(APIView):
    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        tutorial = self.get_object(pk)

        tutorial.like_count += 1
        result = tutorial.save()

        result_data = {
            "success": True,
            "result": result,
        }
        return Response(result_data, status=HTTP_200_OK)
    
class TutorialUnLike(APIView):
    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        tutorial = self.get_object(pk)

        tutorial.unlike_count += 1
        result = tutorial.save()

        result_data = {
            "success": True,
            "result": result,
        }
        return Response(result_data, status=HTTP_200_OK)


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
            tutorial = serializer.save(author=request.user)
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
        print("TutorialDetail view ?????? ?????? !!")
        print(pk, type(pk))
        tutorial = self.get_object(pk)
        # print("Tutorial : ", Tutorial)
        serializer = TutorialDetaailSerializer(
            tutorial, context={"request": request}
        )
        print("/Tutorials/:pk ??? ?????? ?????????????????? ???????????? ????????? serializer.data: ", serializer.data)
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
            print("serializer ?????????")
            try:
                tutorial = serializer.save(author=request.user)
                serializer = TutorialDetaailSerializer(tutorial)
                return Response(serializer.data)

            except Exception as e:
                print("ee : ", e)
                raise ParseError("tutorial not found")
        else:
            print("????????? ???????????? ???????????? ??????")
            raise ParseError("serializer is not valid")

    def delete(self, request, pk):
        print("?????? ?????? ??????")
        tutorial = self.get_object(pk)
        tutorial.delete()
        return Response(status=HTTP_204_NO_CONTENT)
