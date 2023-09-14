from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN
)
from .models import (
    Challenge
)

from .serializers import (
    SerializerForChallenges,
)

# Create your views here.
# ListViewForChallenges
class ListViewForChallenge(APIView):
    # pagination 관련 변수 선언
    listForChallenge = []
    perPage = 10
    totalCountForChallengeList = 0

    def get(self, request):
        # pageNum 받아와서 초기화
        pageNum = request.query_params.get("pageNum", 1)
        pageNum = int(pageNum)

        # suggestion list data 가져 오기
        list_for_challenge = Challenge.objects.all().order_by('-created_at')
        self.listForChallenge = list_for_challenge

        # 총 개수 초기화
        self.totalCountForChallengeList = list_for_challenge.count()

        # 범위 지정 하기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.listForChallenge = self.listForChallenge[start:end]

        # 해당 범위에 대해 listForSuggestionList 직렬화
        serializer = SerializerForChallenges(self.listForChallenge, many=True)

        # 응답용 딕셔너리 선언
        response_data = {
            "listForChallenge": serializer.data,
            "totalCountForChallengeList": self.totalCountForChallengeList,
            "perPage": self.perPage,
        }

        # Response 로 응답용 딕셔너리 와 Http code 전달
        return Response(response_data, status=HTTP_200_OK)