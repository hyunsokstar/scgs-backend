from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from .models import ShortCut
from .serializers import SerializerForInsertToShortcut, ShortCutSerializer


class ShortCutListView(APIView):
    # def get(self, request):
    #     print("shortcut list 요청 받음")
    #     shortcuts = ShortCut.objects.all()
    #     serializer = ShortCutSerializer(shortcuts, many=True)
    #     response_data = {
    #         'success': True,
    #         'shortcut_list': serializer.data,
    #     }
    #     return Response(response_data, status=status.HTTP_200_OK)

    toalCountForShortcut = 0
    per_page = 5

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

        # step7-1 범위 정하기 (start ~ end)
        start = (page - 1) * self.per_page
        end = start + self.per_page
        # step 7-2 해당 범위의 목록 가져 오기
        list_for_shortcut_for_page = self.get_shortcut_list()[start:end]

        # step 8 시리얼라이저로 직렬화 
        serializer = ShortCutSerializer(list_for_shortcut_for_page, many=True)      

        data = {
            "totalCount": self.toalCountForShortcut,
            "shortcut_list": serializer.data
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        # print("request.data['shortcut] : ", request.data['shortcut'])
        # print("request.data['description] : ", request.data['description'])
        # print("request.data['classification] : ",
        #       request.data['classification'])

        serializer = SerializerForInsertToShortcut(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                shortcut = serializer.save(writer=request.user)
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