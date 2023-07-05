import requests
from django.conf import settings
# from project_progress.models import ProjectProgress, TestForTask, TestForExtraTask
from project_progress.models import (
    ProjectProgress,
    ExtraTask,
    TestForTask,
    TestForExtraTask
)
# from medias.serializers import ReferImageForTaskSerializer, TestResultImageSerializer, TestResultImageForExtraTaskSerializer
from medias.serializers import (
    ReferImageForTaskSerializer,
    TestResultImageForCompletedTaskSerializer,
    TestResultImageSerializer,
    TestResultImageForExtraTaskSerializer,
    ReferImageForExtraTaskSerializer
)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from .models import Photo, ReferImageForExtraTask, ReferImageForTask
from rest_framework import status


class CreateViewForResultImageForCompletedTask(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def post(self, request):
        taskPk = request.data["taskPk"]
        project_task = self.get_object(taskPk)

        serializer = TestResultImageForCompletedTaskSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(task=project_task)
            serializer = TestResultImageForCompletedTaskSerializer(photo)
            response_data = {
                "message": "Image upload for completed task is successful.",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestResultImageForExtraTask(APIView):
    def get_object(self, pk):
        try:
            return TestForExtraTask.objects.get(pk=pk)
        except TestForExtraTask.DoesNotExist:
            raise NotFound

    def post(self, request):
        print("request.data[testPk] : ", request.data["testPk"])
        serializer = TestResultImageForExtraTaskSerializer(data=request.data)

        if serializer.is_valid():
            test = self.get_object(request.data["testPk"])
            test_result = serializer.save(test=test)
            print("test_result : ", test_result)
            serializer = TestResultImageForExtraTaskSerializer(test_result)
            print("serializer : ", serializer.data)
            return Response(serializer.data)
        else:
            raise ParseError(serializer.errors)


class createTestImageResult(APIView):
    def get_object(self, pk):
        try:
            return TestForTask.objects.get(pk=pk)
        except TestForTask.DoesNotExist:
            raise NotFound

    def post(self, request):
        print("request.data[testPk] : ", request.data["testPk"])
        serializer = TestResultImageSerializer(data=request.data)

        if serializer.is_valid():
            test = self.get_object(request.data["testPk"])
            test_result = serializer.save(test=test)
            print("test_result : ", test_result)
            serializer = TestResultImageSerializer(test_result)
            print("serializer : ", serializer.data)
            return Response(serializer.data)
        else:
            raise ParseError(serializer.errors)


class DeleteViewForRefImageForExtraTask(APIView):

    def get_object(self, pk):
        try:
            return ReferImageForExtraTask.objects.get(pk=pk)
        except ReferImageForExtraTask.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        ref_image = self.get_object(pk)

        # if room.owner != request.user:
        #     raise PermissionDenied
        ref_image.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class DeleteViewForRefImageForTask(APIView):

    def get_object(self, pk):
        try:
            return ReferImageForTask.objects.get(pk=pk)
        except ReferImageForTask.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        ref_image = self.get_object(pk)

        # if room.owner != request.user:
        #     raise PermissionDenied
        ref_image.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CreateViewForRefImageToExtraTaskDetail(APIView):
    def get_object(self, pk):
        try:
            return ExtraTask.objects.get(pk=pk)
        except ExtraTask.DoesNotExist:
            raise NotFound

    def post(self, request):
        taskPk = request.data["taskPk"]
        # print("request.data[taskPk] : ", request.data["taskPk"])

        extra_task = self.get_object(taskPk)

        serializer = ReferImageForExtraTaskSerializer(
            data=request.data)

        if serializer.is_valid():
            # photo = serializer.save(user=user)
            photo = serializer.save(task=extra_task)
            print("photo : ", photo)
            serializer = ReferImageForTaskSerializer(photo)
            print("serializer : ", serializer.data)
            return Response(serializer.data)
        else:
            raise ParseError(serializer.errors)
            # return Response(serializer.errors)


class CreateViewForRefImageToTaskDetail(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def post(self, request):
        taskPk = request.data["taskPk"]
        # print("request.data[taskPk] : ", request.data["taskPk"])

        project_task = self.get_object(taskPk)

        serializer = ReferImageForTaskSerializer(
            data=request.data)

        if serializer.is_valid():
            # photo = serializer.save(user=user)
            photo = serializer.save(task=project_task)
            print("photo : ", photo)
            serializer = ReferImageForTaskSerializer(photo)
            print("serializer : ", serializer.data)
            return Response(serializer.data)
        else:
            raise ParseError(serializer.errors)
            # return Response(serializer.errors)


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


# https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/images/v2/direct_upload

class GetUploadURL(APIView):
    print("get upload url 뷰 실행")

    def post(self, request):
        print("settings.CF_ID :", settings.CF_ID)
        print("settings.CF_TOKEN :", settings.CF_TOKEN)
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"}
        )

        one_time_url = one_time_url.json()
        # print("in_time_url : ", one_time_url)
        # return Response(one_time_url)

        result = one_time_url.get("result")
        return Response({"id": result.get("id"), "uploadURL": result.get("uploadURL")})
