import requests
from django.conf import settings
from project_progress.models import ProjectProgress
from medias.serializers import ReferImageForTaskSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
# from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated

from .models import Photo


class CreateViewForRefImageToTaskDetail(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except Photo.DoesNotExist:
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
