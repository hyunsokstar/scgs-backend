from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from .models import Suggestion
from .serializers import SerializerForCreateSuggestionForBoard, SuggestionSerializer

# Create Suggestion
class CreateViewForSuggestionForBoard(APIView):
    def post(self, request):
        try:
            print("건의 사항 추가 요청 check for board !!")

            # 필요한 필드 직접 추출
            title = request.data.get("title")
            content = request.data.get("content")

            # 직렬화
            serializer = SerializerForCreateSuggestionForBoard(data={
                "title": title,
                "content": content,
                "writer": request.user.id  # 또는 원하는 작성자 정보
            })

            if serializer.is_valid():
                suggestion = serializer.save()  # create 메서드를 사용하여 저장

                return Response({"message": "건의 사항이 추가되었습니다.", "suggestion_id": suggestion.id}, status=HTTP_201_CREATED)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("에러 발생:", str(e))
            return Response({"message": "건의 사항 추가 중에 오류가 발생했습니다."}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ListViewForSuggestion(APIView):
    # pagination 관련 변수 선언
    listForSuggestion = []
    perPage = 5
    totalCountForSuggestionList = 0

    def get(self, request):
        # pageNum 받아와서 초기화
        pageNum = request.query_params.get("pageNum", 1)
        pageNum = int(pageNum)

        # suggestion list data 가져 오기
        list_for_suggestion = Suggestion.objects.all()
        self.listForSuggestion = list_for_suggestion

        # 총 개수 초기화
        self.totalCountForSuggestionList = list_for_suggestion.count()

        # 범위 지정 하기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.listForSuggestion = self.listForSuggestion[start:end]

        # 해당 범위에 대해 listForSuggestionList 직렬화
        serializer = SuggestionSerializer(self.listForSuggestion, many=True)

        # 응답용 딕셔너리 선언
        response_data = {
            "listForSuggestion": serializer.data,
            "totalCountForSuggestionList": self.totalCountForSuggestionList,
            "perPage": self.perPage,
        }

        # Response 로 응답용 딕셔너리 와 Http code 전달
        return Response(response_data, status=HTTP_200_OK)
