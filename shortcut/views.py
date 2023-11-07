from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from django.http import Http404

from .models import ShortCut, Tags, RelatedShortcut, ShortCutHub
from .serializers import (
    SerializerForInsertToShortcut,
    ShortCutSerializer,
    RelatedShortcutSerializer,
    ShortcutHubSerializer,
)
from django.db import transaction


# 1122
class ListViewForShortCutHub(APIView):
    totalCountForShortCutHub = 1
    listForShortCutHubList = []
    perPage = 4

    def get_all_shortcut_hub_list(self):
        try:
            return ShortCutHub.objects.all()
        except ShortCut.DoesNotExist:
            raise NotFound

    def get(self, request):
        # pagenumber 초기화
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # 해당 범위의 shortcut hub list 가져 오기
        start = (page - 1) * self.perPage
        end = start + self.perPage

        list_for_shortcut_hub_list = self.get_all_shortcut_hub_list()[start:end]

        serializer = ShortcutHubSerializer(list_for_shortcut_hub_list, many=True)

        self.listForShortCutHubList = serializer.data

        self.totalCountForShortCutHub = self.get_all_shortcut_hub_list().count()

        response_data = {
            "listForShortCutHub": self.listForShortCutHubList,
            "totalCountForShortCutHub": self.totalCountForShortCutHub,
            "perPageForShortCutHub": self.perPage,
        }

        return Response(response_data, status=HTTP_200_OK)


class DeleteRelatedShortcutForCheckedRow(APIView):
    def delete(self, request):
        selected_rows = request.data.get("selectedRows", [])

        try:
            # 선택된 RelatedShortcut 모델들을 삭제
            RelatedShortcut.objects.filter(id__in=selected_rows).delete()
            return Response("RelatedShortcut 모델 삭제 성공")
        except Exception as e:
            return Response(str(e), status=500)


class DeketeRekatedShortCutView(APIView):
    def get_object(self, pk):
        try:
            return RelatedShortcut.objects.get(pk=pk)
        except RelatedShortcut.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        related_shortcut = self.get_object(pk)
        related_shortcut.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShortCutListView(APIView):
    toalCountForShortcut = 0
    per_page = 50

    # step4 목록 가져오는 함수 정의
    def get_shortcut_list(self):
        try:
            return ShortCut.objects.all()
        except ShortCut.DoesNotExist:
            raise NotFound

    def get(self, request):
        # step1 page 번호 받아 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 페이지 번호 확인
        print("page : ", page)

        # step5 total_count
        self.toalCountForShortcut = self.get_shortcut_list().count()
        # step6 total_count 확인
        print("총개수 check (self.toalCountForShortcut) : ", self.toalCountForShortcut)

        # 페이지 범위에 대한 shortcut list
        start = (page - 1) * self.per_page
        end = start + self.per_page
        list_for_shortcut_for_page = self.get_shortcut_list()[start:end]

        # step 8 시리얼라이저로 직렬화
        serializer = ShortCutSerializer(list_for_shortcut_for_page, many=True)

        data = {
            "totalCount": self.toalCountForShortcut,
            "shortcut_list": serializer.data,
            "task_number_for_one_page": self.per_page,
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
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
                print("여기에서 에러 발생 !!!!!!", e)
                raise ParseError("tag not found")

            else:
                shortcut = serializer.save()

            serializer = ShortCutSerializer(shortcut)
        else:
            print("serializer.errors : ", serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)

        return Response({"success": True, "data": serializer.data})


class ShortCutDetailView(APIView):
    def get_object(self, pk):
        try:
            return ShortCut.objects.get(pk=pk)
        except ShortCut.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        shortcut = self.get_object(pk)
        shortcut.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        shortcut = self.get_object(pk)
        shortcut_data = request.data

        shortcut.shortcut = shortcut_data.get("shortcut", shortcut.shortcut)
        shortcut.description = shortcut_data.get("description", shortcut.description)
        shortcut.classification = shortcut_data.get(
            "classification", shortcut.classification
        )

        # Clear the existing tags and add new ones
        shortcut.tags.clear()
        for tag_name in shortcut_data.get("tags", []):
            tag, _ = Tags.objects.get_or_create(name=tag_name)
            shortcut.tags.add(tag)

        shortcut.save()

        serializer = ShortCutSerializer(shortcut)
        return Response({"success": True, "data": serializer.data})

    def post(self, request, pk):
        shortcut_id = pk
        shortcut_content = request.data.get("shortcut_content")
        description = request.data.get("description")

        # Create a new RelatedShortcut instance
        related_shortcut = RelatedShortcut.objects.create(
            shortcut_id=shortcut_id,
            shortcut_content=shortcut_content,
            description=description,
        )

        # Serialize the created instance
        serializer = RelatedShortcutSerializer(related_shortcut)

        # Return the serialized data in the response
        return Response(serializer.data)

    def get(self, request, pk):
        shortcut = self.get_object(pk)
        related_shortcuts = RelatedShortcut.objects.filter(shortcut=shortcut)

        shortcut_serializer = ShortCutSerializer(shortcut)
        related_shortcuts_serializer = RelatedShortcutSerializer(
            related_shortcuts, many=True
        )

        data = {
            "data_for_original_shortcut": shortcut_serializer.data,
            "data_for_related_shortcut": related_shortcuts_serializer.data,
        }
        return Response(data, status=HTTP_200_OK)


class RelatedShortcutView(APIView):
    def delete(self, request, pk):
        shortcut = self.get_object(pk)
        shortcut.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        print("shortcut update 요청 확인")
        print("request.data", request.data)
        print("pk : ", pk)
        shortcut = self.get_object(pk)
        print("shortcut : ", shortcut)

        serializer = SerializerForInsertToShortcut(
            shortcut, data=request.data, partial=True
        )

        if serializer.is_valid():
            try:
                shortcut = serializer.save()

                shortcut.tags.clear()
                tags = request.data.get("tags")
                print("tags : ", tags)

                tags = request.data.get("tags")
                for tagName in tags:
                    is_tag_exists = Tags.objects.filter(name=tagName).exists()

                    if is_tag_exists == False:
                        tag = Tags.objects.create(name=tagName)
                        tag.save()

                    tag = Tags.objects.get(name=tagName)
                    print("tag : ", tag)
                    shortcut.tags.add(tag)

                serializer = SerializerForInsertToShortcut(shortcut)
                return Response(serializer.data)

            except Exception as e:
                print("e : ", e)
                raise ParseError("project_task not found")
        else:
            print(serializer.errors)
            raise ParseError("serializer is not valid: {}".format(serializer.errors))
