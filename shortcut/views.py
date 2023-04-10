from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from .models import ShortCut, Tags
from .serializers import SerializerForInsertToShortcut, ShortCutSerializer
from django.db import transaction


class ShortCutListView(APIView):
    def get(self, request):
        print("shortcut list 요청 받음")
        shortcuts = ShortCut.objects.all()
        serializer = ShortCutSerializer(shortcuts, many=True)
        response_data = {
            'success': True,
            'shortcut_list': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # print("request.data['shortcut] : ", request.data['shortcut'])
        # print("request.data['description] : ", request.data['description'])
        # print("request.data['classification] : ",
        #       request.data['classification'])
        serializer = SerializerForInsertToShortcut(data=request.data)

        tags = request.data.get("tags")
        for tagName in tags:
            is_tag_exists = Tags.objects.filter(name=tagName).exists()

            if is_tag_exists == False:
                tag = Tags.objects.create(name=tagName)
                tag.save()

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if request.user.is_authenticated:
                        shortcut = serializer.save(writer=request.user)

                        tags = request.data.get("tags")
                        print("tags : ", tags)
                        for tagName in tags:
                            tag = Tags.objects.get(name=tagName)
                            print("tag : ", tag)
                            shortcut.tags.add(tag)
            except Exception as e:
                print("여기에서 에러 발생 !!!!!!" , e)
                raise ParseError("tag not found")                    

            else:
                shortcut = serializer.save()

            serializer = ShortCutSerializer(shortcut)
        else:
            print("serializer.errors : ", serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)

        return Response({"success": True, "data": serializer.data})

# ShortCutDetailView


class ShortCutDetailView(APIView):
    def get_object(self, pk):
        try:
            return ShortCut.objects.get(pk=pk)
        except ShortCut.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        shortcut = self.get_object(pk)
        shortcut.delete()

        return Response(status=HTTP_204_NO_CONTENT)
