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
    Suggestion,
    CommentForSuggestion,
)
from .serializers import (
    SerializerForCreateSuggestionForBoard,
    SuggestionSerializer,
    SerializerForCommentListForSuggestionForBoard,
    SerializerForCreateCommentForSuggestionForBoard
)

# 1122

class CreateViewForCommentForSuggestionForBoard(APIView):
    def post(self, request, suggestionId):
        print("suggest 댓글 추가 요청 check !!!!!!!!!")
        try:
            print("suggestionId :::::::::::: ", suggestionId)
            # Check if the error_report with the provided error_report_pk exists
            suggestion = Suggestion.objects.get(
                id=suggestionId)

            print("suggestion ::::::::::::: ", suggestion)

        except Suggestion.DoesNotExist:
            return Response(
                {"message": "Error report not found"},
                status=HTTP_404_NOT_FOUND
            )

        print("request.data : ", request.data)

        request.data["suggestion"] = suggestion.id
        serializer = SerializerForCreateCommentForSuggestionForBoard(data=request.data)

        if serializer.is_valid():
            print("시리얼 라이저는 유효")
            print("댓글 추가 요청 확인 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            serializer.save(writer=request.user)

            return Response(
                {"message": "Comment created successfully"},
                status=HTTP_201_CREATED
            )
        else:
            # Return detailed error messages
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST
            )


# CreateViewForCommentForSuggestionForBoard
# class DeleteViewForCommentForSuggestionForBoard(APIView):
#     def delete(self, request, commentPk):
#         try:
#             comment = CommentForSuggestion.objects.get(pk=commentPk)
#         except CommentForSuggestion.DoesNotExist:
#             return Response({"message": "comment not found"}, status=HTTP_404_NOT_FOUND)

#         if request.user != comment.writer:
#             return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

#         comment.delete()

#         return Response({"message": "FAQ deleted successfully"}, status=HTTP_204_NO_CONTENT)

class DeleteViewForCommentForSuggestionForBoard(APIView):
    def delete(self, request, commentPk):
        try:
            comment = CommentForSuggestion.objects.get(pk=commentPk)
        except CommentForSuggestion.DoesNotExist:
            return Response({"message": "comment not found"}, status=HTTP_404_NOT_FOUND)

        if request.user != comment.writer:
            return Response({"message": f"삭제 권한은 {comment.writer.username} 에게 있습니다"}, status=HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({"message": "FAQ deleted successfully"}, status=HTTP_204_NO_CONTENT)

class UpdateViewForFaqComment(APIView):
    def put(self, request, commentPk):
        try:
            # commentPk에 해당하는 댓글 찾기
            comment = CommentForSuggestion.objects.get(pk=commentPk)

            # 요청에서 수정된 내용 가져오기
            editedContent = request.data.get('editedContent')

            # 댓글 업데이트
            comment.content = editedContent
            comment.save()

            # 성공적인 응답
            return Response({'message': 'faq comment update success !!'}, status=HTTP_200_OK)

        except CommentForSuggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response({'message': 'Comment not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            # 다른 예외 처리
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)




class ListViewForCommentForSuggestionForBoard(APIView):
    def get(self, request, suggestionId):
        print("댓글 데이터 요청 확인 for 건의 사항")
        try:
            # suggestionPk 해당하는 CommentForSuggestion 정보 가져오기
            comments = CommentForSuggestion.objects.filter(
                suggestion_id=suggestionId)

            # Serializer를 사용하여 데이터 직렬화
            serializer = SerializerForCommentListForSuggestionForBoard(comments, many=True)

            # 응답 데이터 구성
            response_data = {
                'comments': serializer.data,
            }

            return Response(response_data, status=HTTP_200_OK)
        except CommentForSuggestion.DoesNotExist:
            return Response({'detail': 'Comments not found'}, status=HTTP_404_NOT_FOUND)


# ListViewForCommentForSuggestionForBoard
# DeleteViewForSuggestionForBoard
class DeleteViewForSuggestionForBoard(APIView):
    def delete(self, request, suggestionPk):
        print("삭제 요청 확인 ", suggestionPk)
        try:
            # commentPk에 해당하는 댓글 찾기
            suggestion = Suggestion.objects.get(pk=suggestionPk)

            # 댓글 삭제
            suggestion.delete()

            # 성공적인 응답
            return Response({'message': 'delete comment for faq success'}, status=HTTP_204_NO_CONTENT)

        except Suggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response({'message': 'Comment not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            # 다른 예외 처리
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateViewForSuggestionForBoard(APIView):
    def put(self, request, suggestionPk):

        print("update 요청 받았습니다")
        try:
            # commentPk에 해당하는 댓글 찾기
            suggestion = Suggestion.objects.get(pk=suggestionPk)

            # 요청에서 수정된 내용 가져오기
            editedtitle = request.data.get('title')
            editedContent = request.data.get('content')

            # 댓글 업데이트
            suggestion.title = editedtitle
            suggestion.content = editedContent
            suggestion.save()

            # 성공적인 응답
            return Response({'message': 'faq suggestion update success !!'}, status=HTTP_200_OK)

        except Suggestion.DoesNotExist:
            # 댓글을 찾을 수 없는 경우
            return Response({'message': 'suggestion not found'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            # 다른 예외 처리
            return Response({'message': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


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
