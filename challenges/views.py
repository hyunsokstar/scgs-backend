from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated, ValidationError
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from .models import (
    Challenge,
    EvaluationCriteria,
    EvaluationResult,
    ChallengeResult
)

from .serializers import (
    SerializerForChallenges,
    SerializerForCreateChallenge,
    SerializerForChallengeDetail,
    EvaluationResultSerializer
)

# 1122
# UpdateViewForChallengeResultPassed


class UpdateViewForChallengeResultPassed(APIView):
    def put(self, request, challengeResultId):
        try:

            # challengeId, userName, criteria에 해당하는 EvaluationResult 조회
            challenge_result = ChallengeResult.objects.get(
                id=challengeResultId,
            )

            print("evaluation_result for check : ", challenge_result)
            print("result for check : ", challenge_result.pass_status)

            # 결과를 업데이트하고 저장합니다.
            if challenge_result.pass_status:
                challenge_result.pass_status = False
            else:
                challenge_result.pass_status = True

            # 업데이트된 결과를 저장
            challenge_result.save()

            message = f"passed_status 를 {challenge_result.pass_status} 로 업데이트 했습니다."

            # 업데이트된 결과를 응답으로 반환
            return Response({"message": message}, status=HTTP_200_OK)

        except ChallengeResult.DoesNotExist:
            return Response({"message": "해당 EvaluationResult를 찾을 수 없습니다."}, status=HTTP_404_NOT_FOUND)

        except Exception as e:
            # 기타 예외 처리
            return Response({"message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

# UpdateViewForChallengeResultPassed


class UpdateViewForEvaluateResultForChallenge(APIView):
    def put(self, request, challengeId):
        try:

            # challengeId, userName, criteria에 해당하는 EvaluationResult 조회
            evaluation_result = EvaluationResult.objects.get(
                challenge_id=challengeId,
                challenger__username=request.data.get("userName"),
                evaluate_criteria_description=request.data.get("criteria"),
            )

            print("evaluation_result for check : ", evaluation_result)
            print("result for check : ", evaluation_result.result)

            # 결과를 업데이트하고 저장합니다.
            if evaluation_result.result == "fail" or evaluation_result.result == "undecided":
                print("pass 로 업데이트")
                evaluation_result.result = "pass"
            else:
                print("fail 로 update")
                evaluation_result.result = "fail"

            # 업데이트된 결과를 저장
            evaluation_result.save()

            # 업데이트된 결과를 응답으로 반환
            return Response({"message": "업데이트가 성공적으로 수행되었습니다."}, status=HTTP_200_OK)

        except EvaluationResult.DoesNotExist:
            # EvaluationResult가 존재하지 않을 때의 처리
            return Response({"message": "해당 EvaluationResult를 찾을 수 없습니다."}, status=HTTP_404_NOT_FOUND)

        except Exception as e:
            # 기타 예외 처리
            return Response({"message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class WithDrawlViewForChallenge(APIView):
    def delete(self, request, challengeId):
        try:
            evaluate_result = EvaluationResult.objects.filter(
                challenge_id=challengeId, challenger=request.user)
            evaluate_result.delete()

            challenge_result = ChallengeResult.objects.filter(
                challenge_id=challengeId, challenger=request.user)
            challenge_result.delete()

            return Response(status=HTTP_204_NO_CONTENT)
        except EvaluationResult.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


# class ReigsterViewForChallenge(APIView):
#     def post(self, request, challengeId):
#         if not request.user.is_authenticated:
#             return Response(
#                 {"message": "로그인 안한 유저는 challenge 에 register 불가 !"},
#                 status=HTTP_401_UNAUTHORIZED
#             )

#         # todo
#         # EvaluationCriteria 데이터를 필터링한 데이터 (by challengeId)의 개수만큼
#         # EvaluationResult 데이터를 생성
#         # 단, EvaluationResult.evaluate_criteria_description = EvaluationCriteria.item_description
#         # 적절한 Response 응답 with message: challenge 에 대한 등록 완료


class ReigsterViewForChallenge(APIView):
    def post(self, request, challengeId):

        # 이미 등록한 경우 처리
        existing_evaluation = EvaluationResult.objects.filter(
            challenge=challengeId, challenger=request.user)
        if existing_evaluation.exists():
            return Response({"message": "이미 등록했습니다."}, status=HTTP_409_CONFLICT)

        if not request.user.is_authenticated:
            return Response({"message": "로그인 안한 유저는 challenge 에 register 불가 !"}, status=HTTP_401_UNAUTHORIZED)

        try:
            challenge = Challenge.objects.get(pk=challengeId)
        except Challenge.DoesNotExist:
            raise Http404("Challenge does not exist")

        evaluation_criteria_list = EvaluationCriteria.objects.filter(
            challenge=challenge)

        # evaluation_criteria_list의 검색 결과가 0개일 경우
        if not evaluation_criteria_list.exists():
            return Response({"message": "아직 평가 기준이 없으므로 등록 할수 없습니다."}, status=HTTP_400_BAD_REQUEST)

        for evaluation_criteria in evaluation_criteria_list:
            EvaluationResult.objects.create(
                challenger=request.user,
                challenge=challenge,
                evaluate_criteria_description=evaluation_criteria.item_description,
                result="undecided"
            )
        
        ChallengeResult.objects.create(
            challenger = request.user,
            challenge=challenge
        )

        return Response({"message": f"{challenge.title}에 대한 등록 완료"}, status=HTTP_201_CREATED)

# http://127.0.0.1:8000/api/v1/challenges/5/detail


class DetailViewForChallenge(APIView):
    def get(self, request, challengeId):
        try:
            # challengeId에 해당하는 Challenge 모델 인스턴스 조회
            challenge = Challenge.objects.get(id=challengeId)

            # Challenge 모델 인스턴스를 Serializer를 통해 직렬화
            # serializer = SerializerForChallengeDetail(challenge)
            serializer = SerializerForChallengeDetail(
                challenge, context={'request': request})

            # 직렬화된 데이터를 JSON 응답으로 반환
            return Response(serializer.data, status=HTTP_200_OK)

        except Challenge.DoesNotExist:
            # Challenge 모델 인스턴스가 존재하지 않는 경우 404 응답 반환
            return Response({"error": "Challenge not found"}, status=HTTP_404_NOT_FOUND)


class SaveViewForEvaluationCriteriaForChallenge(APIView):
    def post(self, request, challengeId):
        # challengeId는 URL에서 가져올 수 있습니다.
        print(challengeId)

        # 요청에서 데이터를 가져옵니다.
        RowsDataForSave = request.data.get('RowsDataForSave', [])

        # 받은 데이터를 처리합니다.
        updated_count = 0
        added_count = 0

        for row_data in RowsDataForSave:
            item_id = row_data.get('id')
            item_description = row_data.get('item_description')

            if item_id == "new_id":
                # UUID가 있는 경우 새로운 항목 생성
                challenge = Challenge.objects.get(id=challengeId)
                criteria = EvaluationCriteria(
                    challenge=challenge,
                    item_description=item_description
                )
                criteria.save()
                added_count += 1
            else:
                # UUID가 아닌 경우 해당 ID를 사용하여 기존 항목 업데이트
                try:
                    criteria = EvaluationCriteria.objects.get(id=item_id)
                    criteria.item_description = item_description
                    criteria.save()
                    updated_count += 1
                except EvaluationCriteria.DoesNotExist:
                    pass

        # 적절한 응답과 메시지를 반환합니다.
        response_data = {
            'message': f'평가 기준에 대해 {updated_count}개 업데이트 {added_count}개 추가 했습니다.',
            'data': {
                'updated_count': updated_count,
                'added_count': added_count,
            }
        }

        return Response(response_data, status=HTTP_201_CREATED)

# ReigsterViewForChallenge


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


# DetailViewForChallenge
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
