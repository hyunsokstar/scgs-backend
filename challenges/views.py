from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated, ValidationError

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    ChallengeRef,
    EvaluationCriteria,
    EvaluationResult,
    ChallengeResult,
    ChallengeComment
)

from .serializers import (
    SerializerForChallengeRef,
    SerializerForChallenges,
    SerializerForCreateChallenge,
    SerializerForChallengeDetail,
    EvaluationResultSerializer
)

# 1122
class CreateViewForChallengeRef(APIView):

    def post(self, request, challengeId):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인 안한 유저는 challenge ref 생성 못해요 !"},
                status=HTTP_401_UNAUTHORIZED
            )

        try:
            challenge = Challenge.objects.get(id=challengeId)

            # challenge.writer 와 request.user 즉 로그인 유저가 다르면 
            # message challenge.writer.username 님만 ref 를 추가 가능합니다 응답
            if challenge.writer != request.user:
                return Response(
                    {"message": f"{challenge.writer.username} 님만 ref 를 추가 가능합니다."},
                    status=HTTP_400_BAD_REQUEST
                )

            # 댓글 생성
            urlText = request.data.get("urlText")
            descriptionText = request.data.get("descriptionText")

            if urlText and descriptionText:
                ChallengeRef.objects.create(
                    challenge=challenge,
                    url=urlText,
                    description=descriptionText,
                )
                return Response(
                    {"message": "ChallengeRef is Successfully Created"},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "댓글 텍스트가 비어 있습니다."},
                    status=HTTP_400_BAD_REQUEST
                )

        except Challenge.DoesNotExist:
            return Response(
                {"message": "해당하는 Challenge를 찾을 수 없습니다."},
                status=HTTP_404_NOT_FOUND
            )

# UpdateViewForChallengeRef
class UpdateViewForChallengeRef(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, challengeRefId):
        try:
            return ChallengeRef.objects.get(id=challengeRefId)
        except ChallengeRef.DoesNotExist:
            raise NotFound

    def put(self, request, challengeRefId):
        challenge_ref = self.get_object(challengeRefId)  # 개별 유저 가져 오기

        # 요청 데이터에서 이미지 가져오기
        urlText = request.data.get("urlText")
        descriptionText = request.data.get("descriptionText")

        print("challengeRefId:", challengeRefId)
        print("urlTet:", urlText)
        print("descriptionText:", descriptionText)

        try:
            # 이미지 업데이트
            challenge_ref.url = urlText
            challenge_ref.description = descriptionText
            challenge_ref.save()

            # 업데이트 성공 응답
            return Response({"message": "challenge ref is updated"}, status=HTTP_200_OK)
        except Exception as e:
            # 예외 처리: 데이터베이스 작업 중 오류가 발생한 경우
            return Response({"message": f"An error occurred: {str(e)}"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

# ListViewForChallengeRef


class ListViewForChallengeRef(APIView):
    def get(self, request, challengeId):
        try:
            # 주어진 challengeId에 해당하는 Challenge 조회
            challenge = Challenge.objects.get(id=challengeId)

            # ChallengeRef 목록 조회
            challenge_refs = ChallengeRef.objects.filter(challenge=challenge)

            # 시리얼라이즈
            serializer = SerializerForChallengeRef(challenge_refs, many=True)

            # 응답 데이터 구성
            response_data = {
                # "challenge": SerializerForChallenges(challenge).data,
                "challengeRefList": serializer.data
            }

            return Response(response_data, status=HTTP_200_OK)

        except Challenge.DoesNotExist:
            # 주어진 challengeId에 해당하는 Challenge가 존재하지 않는 경우
            return Response({"error": "Challenge not found"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            # 다른 예외 발생 시
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


# DeleteViewForCommentForChallenge
class DeleteViewForCommentForChallenge(APIView):
    def delete(self, request, commentId):
        try:
            challenge_comment = ChallengeComment.objects.get(id=commentId)
            challenge_comment.delete()

            message = f"${challenge_comment} 를 삭제 했습니다."

            return Response({message: message}, status=HTTP_204_NO_CONTENT)
        except ChallengeComment.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


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


class CreateViewForCommentForChallenge(APIView):
    writer_classfication_option = "commenter"

    def post(self, request, challengeId):
        if not request.user.is_authenticated:
            return Response(
                {"message": "로그인 안한 유저는 challenge comment 생성 못해요 !"},
                status=HTTP_401_UNAUTHORIZED
            )

        try:
            # challengeId에 해당하는 Challenge 찾기
            challenge = Challenge.objects.get(id=challengeId)
            participant_username = request.data.get("participant_username")
            print("participant_username :: ", participant_username)

            if request.user == challenge.writer:
                self.writer_classfication_option = "commenter"
            elif request.user.username == participant_username:
                self.writer_classfication_option = "challenger"
            else:
                self.writer_classfication_option = "participant"

            # 댓글 생성
            comment_text = request.data.get("commentText")
            if comment_text:
                ChallengeComment.objects.create(
                    challenge=challenge,
                    writer=request.user,
                    challenger=request.user,
                    comment=comment_text,
                    writer_classfication=self.writer_classfication_option
                )

                return Response(
                    {"message": "댓글이 성공적으로 생성되었습니다."},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "댓글 텍스트가 비어 있습니다."},
                    status=HTTP_400_BAD_REQUEST
                )

        except Challenge.DoesNotExist:
            return Response(
                {"message": "해당하는 Challenge를 찾을 수 없습니다."},
                status=HTTP_404_NOT_FOUND
            )


@method_decorator(login_required, name='dispatch')
class UpdateViewForChallengeResultMetaInfo(APIView):
    def put(self, request, challengeResultId):
        try:
            # challengeResultId에 해당하는 ChallengeResult 객체 가져오기
            challenge_result = ChallengeResult.objects.get(
                id=challengeResultId)

            # 현재 사용자가 ChallengeResult의 challenger와 일치하는지 확인
            if challenge_result.challenger.username != request.user.username:
                return Response(
                    {"message": "해당 ChallengeResult를 업데이트할 권한이 없습니다."},
                    status=HTTP_403_FORBIDDEN
                )

            # 요청에서 전달된 데이터 가져오기
            github_url1 = request.data.get("github_url1")
            github_url2 = request.data.get("github_url2")
            note_url = request.data.get("note_url")

            # 받은 데이터로 필드를 업데이트
            challenge_result.github_url1 = github_url1
            challenge_result.github_url2 = github_url2
            challenge_result.note_url = note_url

            # 변경사항 저장
            challenge_result.save()

            return Response(
                {"message": f"{challenge_result.challenge.title}에 대한 업데이트 성공"},
                status=HTTP_200_OK
            )
        except ChallengeResult.DoesNotExist:
            return Response(
                {"message": "해당 ChallengeResult를 찾을 수 없습니다."},
                status=HTTP_404_NOT_FOUND
            )


# UpdateViewForChallenge
@method_decorator(login_required, name='dispatch')
class UpdateViewForChallenge(APIView):
    def put(self, request, challengeId):
        # Challenge를 찾습니다. 존재하지 않으면 404 에러 반환
        challenge = get_object_or_404(Challenge, pk=challengeId)

        # 로그인한 유저와 Challenge의 작성자가 다를 경우 에러 응답
        if challenge.writer != request.user:
            return Response({"message": "로그인 유저가 아닐 경우 업데이트 할 수 없습니다."}, status=HTTP_403_FORBIDDEN)

        # 요청에서 전달받은 데이터로 Challenge 업데이트
        challenge.title = request.data.get("title", challenge.title)
        challenge.subtitle = request.data.get("subtitle", challenge.subtitle)
        challenge.description = request.data.get(
            "description", challenge.description)
        challenge.started_at = request.data.get(
            "started_at", challenge.started_at)
        challenge.deadline = request.data.get("deadline", challenge.deadline)

        challenge.save()

        return Response({"message": f"{challenge.title}에 대한 업데이트 성공"}, status=HTTP_200_OK)


class DeleteViewForChallenge(APIView):
    def delete(self, request, challengeId):
        try:
            challenge = Challenge.objects.get(id=challengeId)
            challenge.delete()

            message = f'${challenge.title} delete success !'

            return Response({"message": message}, status=HTTP_204_NO_CONTENT)
        except EvaluationResult.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


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

# UpdateViewForChallenge


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

# DeleteViewForCommentForChallenge


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
            challenger=request.user,
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

# CreateViewForCommentForChallenge


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
