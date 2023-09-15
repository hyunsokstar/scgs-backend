from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated, ValidationError
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
)

from .models import (
    Challenge
)

from .serializers import (
    SerializerForChallenges,
    SerializerForCreateChallenge
)

# 1122 Create your views here.
class CreateViewForChallenge(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인 안한 유저는 challenge 생성 못해요 !"},
                status=HTTP_401_UNAUTHORIZED
            )

        serializer = SerializerForCreateChallenge(data=request.data)

        if serializer.is_valid():
            # 데이터베이스에 새로운 Challenge 생성
            challenge = serializer.save(writer=request.user)

            return Response(
                {"message": "Challenge 생성 성공", "challenge_id": challenge.id},
                status=HTTP_201_CREATED
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST
            )


class UpdateViewForChallengeMainImage(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, challengeId):
        try:
            return Challenge.objects.get(id=challengeId)
        except Challenge.DoesNotExist:
            raise NotFound

    def put(self, request, challengeId):
        challenge = self.get_object(challengeId)  # 개별 유저 가져 오기

        if request.user != challenge.writer:
            print("403 ??????????")
            message = f"{challenge.writer.username} 님만 이미지를 업데이트 할 수 있습니다."
            return Response({"message": message}, status=HTTP_403_FORBIDDEN)

        # 요청 데이터에서 이미지 가져오기
        image_to_update = request.data.get("image_to_update")

        if image_to_update:
            # 이미지 업데이트
            challenge.main_image = image_to_update
            challenge.save()

            # 업데이트 성공 응답
            return Response({"message": "Challenge main image updated successfully!"}, status=HTTP_200_OK)
        else:
            return Response({"message": "No image provided for update."}, status=HTTP_400_BAD_REQUEST)


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
