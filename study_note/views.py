from django.db import transaction
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CoWriterForStudyNote, StudyNote, StudyNoteContent
from .serializers import (
    SerializerForCreateQuestionForNote,
    StudyNoteContentSerializer,
    StudyNoteSerializer,
    StudyNoteBriefingBoardSerializer,
    CreateCommentSerializerForNote,
    ClassRoomForStudyNoteSerializer,
    QnABoardSerializer,
    ErrorReportForStudyNoteSerializer,
    SerializerForCreateErrorReportForNote,
    FAQBoardSerializer
)

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
import random
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudyNoteContent
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models import Q, F

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min
from django.db import models
from .models import (
    StudyNoteContent,
    ClassRoomForStudyNote,
    StudyNoteBriefingBoard,
    AnswerForQaBoard,
    ErrorReportForStudyNote,
    QnABoard,
    FAQBoard,
)
from django.utils import timezone


# 1122

class UpdateViewForNoteSubtitle(APIView):

    def put(self, request, content_pk, format=None):
        study_note_content = StudyNoteContent.objects.get(pk=content_pk)

        study_note_content.title = request.data.get(
            'title', study_note_content.title)
        study_note_content.content = request.data.get(
            'content', study_note_content.content)
        study_note_content.ref_url1 = request.data.get(
            'ref_url1', study_note_content.ref_url1)
        study_note_content.ref_url2 = request.data.get(
            'ref_url2', study_note_content.ref_url2)
        study_note_content.youtube_url = request.data.get(
            'youtube_url', study_note_content.youtube_url)

        study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class DeleteViewForStudyNote(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def delete(self, request, notePk):
        api_docu = self.get_object(notePk)
        api_docu.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class DeleteViewForErrorReport(APIView):
    def delete(self, request, error_report_pk):
        try:
            error_report = ErrorReportForStudyNote.objects.get(
                pk=error_report_pk)

            if request.user.is_authenticated:
                error_report.delete()
                return Response({"message": "delete ErrorReport success"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "에러 노트를 삭제 할수 없습니다 로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except ErrorReportForStudyNote.DoesNotExist:
            print("ErrorReport is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateViewForErrorReport(APIView):
    def put(self, request, error_report_pk):
        try:
            contentForUpdate = request.data.get("content")
            answer = ErrorReportForStudyNote.objects.get(pk=error_report_pk)

            if request.user.is_authenticated:
                writer = request.user
                # todo commentPk 에 해당하는 answer 의 content 를 위에서 얻은 content 로 수정
                answer.content = contentForUpdate
                answer.save()

                # todo 적당한 http 응답 message 는 comment update success
                return Response({"message": "ErrorReport content update success"}, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except ErrorReportForStudyNote.DoesNotExist:
            print("ErrorReport is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateViewForErrorRecordForNote(APIView):
    def get_object(self, study_note_pk):
        try:
            return StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, study_note_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # study_note_pk에 해당하는 StudyNote 가져오기
        study_note = self.get_object(study_note_pk)

        serializer = SerializerForCreateErrorReportForNote(data=request.data)

        if serializer.is_valid():
            try:
                question = serializer.save(
                    writer=request.user, study_note=study_note)  # study_note 정보 추가
                serializer = SerializerForCreateErrorReportForNote(question)
                return Response({'success': True, "result": serializer.data}, status=HTTP_200_OK)
            except Exception as e:
                print("e: ", e)
                raise ParseError(
                    "An error occurred while serializing the create question data")
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ErrorReportForStudyNoteView(APIView):
    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
            error_reports = study_note.error_reports.all()
            serializer = ErrorReportForStudyNoteSerializer(
                error_reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudyNote.DoesNotExist:
            return Response({"error": "StudyNote not found."}, status=status.HTTP_404_NOT_FOUND)


class ErrorReportForPageForStudyNoteView(APIView):
    def get(self, request, study_note_pk, page):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
            error_reports = study_note.error_reports.filter(page=page)
            serializer = ErrorReportForStudyNoteSerializer(
                error_reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudyNote.DoesNotExist:
            return Response({"error": "StudyNote not found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteViewForCommentForQuestionForNote(APIView):
    def delete(self, request, commentPk):
        try:
            comment = AnswerForQaBoard.objects.get(pk=commentPk)
            comment.delete()
            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except AnswerForQaBoard.DoesNotExist:
            return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateViewForCommentForQuestionForNote(APIView):
    def put(self, request, commentPk):
        try:
            contentForUpdate = request.data.get("content")
            answer = AnswerForQaBoard.objects.get(pk=commentPk)

            if request.user.is_authenticated:
                writer = request.user
                # todo commentPk 에 해당하는 answer 의 content 를 위에서 얻은 content 로 수정
                answer.content = contentForUpdate
                answer.save()

                # todo 적당한 http 응답 message 는 comment update success
                return Response({"message": "Comment update success"}, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except AnswerForQaBoard.DoesNotExist:
            print("AnswerForQaBoard is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateViewForCommentForQuestionForNote(APIView):
    def post(self, request, question_pk):
        try:
            question = QnABoard.objects.get(pk=question_pk)
            content = request.data.get("content")

            if request.user.is_authenticated:
                writer = request.user

                if content:
                    answer = AnswerForQaBoard(
                        question=question, content=content, writer=writer)
                    answer.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    print("content 가 없습니다")
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "댓글을 입력할 수 없습니다. 로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except QnABoard.DoesNotExist:
            print("qa board is note exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteViewForQuestionBoard(APIView):
    def delete(self, request, question_pk):
        try:
            question = QnABoard.objects.get(pk=question_pk)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QnABoard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateViewForQnABoard(APIView):
    def get_object(self, question_pk):
        try:
            return QnABoard.objects.get(pk=question_pk)
        except QnABoard.DoesNotExist:
            raise NotFound

    def put(self, request, question_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        print("question_pk !!!!!!!!!!!!! : ", question_pk)
        qna_board = self.get_object(question_pk)
        if qna_board.writer != request.user:
            raise PermissionDenied

        # 업데이트할 데이터 받기
        title = request.data.get("title")
        content = request.data.get("content")
        page = request.data.get("page")

        # 필요한 필드 업데이트
        qna_board.title = title
        qna_board.content = content
        qna_board.page = page
        qna_board.updated_at = timezone.now()

        # 저장
        qna_board.save()

        return Response(status=status.HTTP_200_OK)


class CreateViewForQnABoard(APIView):
    def get_object(self, study_note_pk):
        try:
            return StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, study_note_pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # study_note_pk에 해당하는 StudyNote 가져오기
        study_note = self.get_object(study_note_pk)

        serializer = SerializerForCreateQuestionForNote(data=request.data)

        if serializer.is_valid():
            try:
                question = serializer.save(
                    writer=request.user, study_note=study_note)  # study_note 정보 추가
                serializer = SerializerForCreateQuestionForNote(question)
                return Response({'success': True, "result": serializer.data}, status=HTTP_200_OK)
            except Exception as e:
                print("e: ", e)
                raise ParseError(
                    "An error occurred while serializing the create question data")
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)


# class QnABoardView(APIView):
#     def get(self, request, study_note_pk):
#         print("study_note_pk : ", study_note_pk)
#         try:
#             study_note = StudyNote.objects.get(pk=study_note_pk)
#         except StudyNote.DoesNotExist:
#             return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

#         qa_list = study_note.question_list.all()
#         serializer = QnABoardSerializer(
#             qa_list, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

class FAQBoardView(APIView):
    def get(self, request, study_note_pk):
        print("study_note_pk : ", study_note_pk)
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        qa_list = study_note.faq_list.all()  # FAQBoard 모델과 연결된 related_name인 "faq_list" 사용
        serializer = FAQBoardSerializer(qa_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class QnABoardView(APIView):
    def get(self, request, study_note_pk):
        print("study_note_pk:", study_note_pk)
        note_page_num = request.query_params.get("note_page_num", None)

        print("note_page_num ::::::::::::::::???????", note_page_num)

        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        if note_page_num is not None:
            qa_list = QnABoard.objects.filter(
                Q(study_note=study_note) & Q(
                    page=note_page_num)
            )
        else:
            qa_list = QnABoard.objects.filter(
                study_note=study_note)

        serializer = QnABoardSerializer(qa_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSavedPageForCurrentNote(APIView):
    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(
                pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        # todo
        # login 안했으면 로그인 사용자가 아닐 경우 저장된 페이지를 불러 올수 없습니다라고 메세지 응답
        if not request.user.is_authenticated:
            print("비로그인 유저에 대한 체크 실행 !")
            return Response("Please log in to retrieve the saved page", status=status.HTTP_401_UNAUTHORIZED)

        existing_class_room = ClassRoomForStudyNote.objects.filter(
            current_note=study_note,
            writer=request.user
        ).exists()

        if existing_class_room:
            class_room = ClassRoomForStudyNote.objects.filter(
                current_note=study_note, writer=request.user).first()
            current_page = class_room.current_page  # class_room.current_page를 변수로 추출
            print("current_page : ", current_page)
            return Response({"current_page": current_page}, status=status.HTTP_200_OK)
        else:
            return Response("saved_data is not exist",
                            status=status.HTTP_404_NOT_FOUND)


class ClasssRoomView(APIView):

    def get_object(self, taskPk):
        try:
            return StudyNote.objects.get(pk=taskPk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        class_list = study_note.class_list.all()
        serializer = ClassRoomForStudyNoteSerializer(
            class_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, study_note_pk):
        # print("실행 check !!!!!!!!!!!!!!!!!!!!!!!!!!")
        try:
            study_note = self.get_object(study_note_pk)
        except StudyNote.DoesNotExist:
            print("여기 실행 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response("Please log in", status=status.HTTP_401_UNAUTHORIZED)

        writer = request.user
        current_page = int(request.data.get("current_page"))

        # Check if a ClassRoomForStudyNote already exists with current_note=study_note
        existing_class_room = ClassRoomForStudyNote.objects.filter(
            current_note=study_note,
            writer=request.user
        ).exists()

        # todo
        # existing_class_room 이 true 이지만 existing_class_room.current_page 와 current_page 가 다를 경우
        # existing_class_room.current_page = current_page 로 업데이트 후
        # return Response("current page num is update to current_page(전달 받은값)", status=status.HTTP_409_CONFLICT)

        if existing_class_room:
            existing_class_room = ClassRoomForStudyNote.objects.filter(
                current_note=study_note, writer=request.user).first()
            if existing_class_room.current_page != current_page:
                print("original : ", existing_class_room.current_page)
                print("current_page : ", current_page)
                print("original type: ", type(existing_class_room.current_page))
                print("current_page type: ", type(current_page))
                existing_class_room.current_page = current_page
                existing_class_room.save()

                response_data = {
                    'save_page_num': current_page
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                print("페이지 번호가 다르지 않습니다")
        # update
        if existing_class_room:
            return Response({"message_type": "warnning", "message": "The record for the current page already exists, so it will not be updated"}, status=status.HTTP_400_BAD_REQUEST)

        print("excute check !!")

        class_room = ClassRoomForStudyNote.objects.create(
            current_note=study_note,
            current_page=current_page,
            writer=writer
        )

        response_data = {
            'save_page_num': current_page
        }

        # serializer = ClassRoomForStudyNoteSerializer(class_room)
        return Response(response_data, status=status.HTTP_201_CREATED)

# UpdateViewForStudyNoteComment


class UpdateViewForStudyNoteComment(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def put(self, request, commentPk):
        print("put 요청 확인")
        print("request.data.get(comment) : ", request.data.get("comment"))
        comment_obj = self.get_object(commentPk)
        comment_obj.comment = request.data.get("comment")
        comment_obj.is_edit_mode = False
        comment_obj.save()

        result_data = {
            "success": True,
            "message": "comment text update success",
        }

        return Response(result_data, status=HTTP_200_OK)


class CreateViewForCommentForNote(APIView):
    def get_object(self, taskPk):
        try:
            return StudyNote.objects.get(pk=taskPk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def post(self, request, studyNotePk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = CreateCommentSerializerForNote(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                # original_task = self.get_object(taskPk)
                test_for_task = serializer.save(writer=request.user)
                serializer = CreateCommentSerializerForNote(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)
            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")
        else:
            print("serializer is not valid !!!!!!!!!!!!")
            print("Errors:", serializer.errors)


class DeleteViewForStudyNoteComment(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def delete(self, request, commentPk):
        comment_obj = self.get_object(commentPk)
        comment_obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class UpdateViewForEditModeForStudyNoteBriefingBoard(APIView):
    def get_object(self, pk):
        try:
            return StudyNoteBriefingBoard.objects.get(pk=pk)
        except StudyNoteBriefingBoard.DoesNotExist:
            raise NotFound

    def put(self, request, commentPk):
        print("put 요청 확인")
        message = ""
        comment = self.get_object(commentPk)

        if comment.is_edit_mode:
            comment.is_edit_mode = False
            message = "edit mode to read mode"

        else:
            comment.is_edit_mode = True
            message = "from read mode to edit mode"

        comment.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class ListViewForStudyNoteBriefingBoard(APIView):
    def get(self, request, study_note_pk):
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response("StudyNote does not exist", status=status.HTTP_404_NOT_FOUND)

        briefing_boards = study_note.note_comments.all()
        serializer = StudyNoteBriefingBoardSerializer(
            briefing_boards, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiViewForGetSubtitleListForNote(APIView):
    def get(self, request, study_note_pk):
        # study_note_pk(StudyNote의 id임)를 참조하는 StudyNoteContent 리스트를 가져옴
        note_contents = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, content_option='subtitle_for_page').order_by('page')

        # 시리얼라이저로 응답 데이터 직렬화
        serializer = StudyNoteContentSerializer(note_contents, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateViewForYoutubeContentForNote(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        content_option = request.data["content_option"]
        title = request.data["title"]
        youtube_url = request.data["youtube_url"]

        max_order = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, page=current_page_number).aggregate(Max('order'))['order__max'] or 0

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            page=current_page_number,
            order=max_order + 1,  # 이전 order 값 중 최대값에 1을 더하여 설정
            writer=request.user,  # 작성자는 현재 요청한 유저로 설정
            content_option=content_option,
            title=title,
            youtube_url=youtube_url,
        )

        print("note_content : ", note_content)

        return Response(
            {
                "message": "youtube content is created successfuly"
            },
            status=status.HTTP_201_CREATED
        )


class CreateViewForSubTitleForNote(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        content_option = request.data["content_option"]
        title = request.data["title"]
        ref_url1 = request.data["ref_url1"]
        ref_url2 = request.data["ref_url2"]
        content = request.data["content"]
        youtube_url = request.data["youtube_url"]

        print("content_option : ", content_option)
        # 이미 sub title for page가 존재하는지 확인
        existing_subtitle = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk,
            page=current_page_number,
            content_option="subtitle_for_page"
        ).exists()

        if existing_subtitle:
            return Response(
                {"message": "If a sub title for the page already exists, The note will not be updated"},
                status=status.HTTP_201_CREATED
            )

        # 이전 order 값 중 최소값 구하기
        min_order = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, page=current_page_number
        ).aggregate(Min('order'))['order__min'] or 0

        # 기존의 min_order가 1인 경우, 기존의 order를 모두 +1 증가
        if min_order == 1:
            StudyNoteContent.objects.filter(
                study_note_id=study_note_pk, page=current_page_number
            ).update(order=models.F('order') + 1)

        if min_order > 1:
            order_for_update = min_order - 1
        else:
            order_for_update = 1

        # Create StudyNoteContent model
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            page=current_page_number,
            content_option=content_option,
            writer=request.user,  # Set the current user as the writer
            order=order_for_update,  # Set the order value
            title=title,
            ref_url1=ref_url1,
            ref_url2=ref_url2,
            content=content
        )

        # Save youtube_url only if it is not empty
        if youtube_url != "":
            note_content.youtube_url = youtube_url
            note_content.save()

        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)


class ApiViewForCoWriter(APIView):
    def delete(self, request, co_writer_pk):
        try:
            co_writer = CoWriterForStudyNote.objects.get(pk=co_writer_pk)
        except CoWriterForStudyNote.DoesNotExist:
            return Response(
                {"message": "CoWriterForStudyNote does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        co_writer.delete()

        return Response(
            {"message": "CoWriterForStudyNote has been deleted successfully."},
            status=status.HTTP_200_OK
        )


class CreateViewForCoWriterForOhterUserNote(APIView):
    def post(self, request, notePk):
        try:
            study_note = StudyNote.objects.get(pk=notePk)
        except StudyNote.DoesNotExist:
            return Response(
                {"message": "StudyNote does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if study_note.writer == request.user:
            return Response(
                {"message": "You cannot request to be a co-writer for your own StudyNote."},
                status=status.HTTP_400_BAD_REQUEST
            )

        co_writer, created = CoWriterForStudyNote.objects.get_or_create(
            writer=request.user,
            study_note=study_note
        )

        if created:
            message = f"{request.user.username}님의 StudyNote에 대한 CoWriter 요청이 성공하였습니다."
        else:
            message = f"{request.user.username}님은 이미 이 StudyNote의 CoWriter입니다."

        return Response(
            {"message": message},
            status=status.HTTP_201_CREATED
        )


class UpdateViewForIsApprovedForCoWorker(APIView):
    def get_cowriter_obj(self, pk):
        try:
            return CoWriterForStudyNote.objects.get(pk=pk)
        except CoWriterForStudyNote.DoesNotExist:
            print("note found !!!!!!!!!!!!!!!!!!!!!!!!")
            raise NotFound

    def post(self, request):
        print("UpdateViewForIsApprovedForCoWorker ?????")
        pass

    def put(self, request):
        print("update-is-approved-for-cowriter for check !!!!!!!!!!!!!!!!!")
        # Use the same key "cowriterPk" as sent from the frontend
        cowriter_pk = request.data.get("cowriterPk")

        cowirter = self.get_cowriter_obj(pk=cowriter_pk)

        # 업데이트할 값 설정 후 save()
        if cowirter.is_approved:
            message = "승인에서 비승인으로 update"
            cowirter.is_approved = False

        else:
            message = "비승인에서 승인으로 update"
            cowirter.is_approved = True

        cowirter.save()

        result_data = {
            "success": True,
            "message":  message
        }

        return Response(result_data, status=HTTP_200_OK)


class CopyCopySelectedNotesToMyNoteView(APIView):
    def post(self, request):
        selectedRowPksFromOriginalTable = request.data.get(
            'selectedRowPksFromOriginalTable')
        print("selectedRowPksFromOriginalTable : ",
              selectedRowPksFromOriginalTable)  # [17,18] <=> StudyNote의 pk

        with transaction.atomic():
            try:
                user = request.user

                # selectedRowPksFromOriginalTable에 해당하는 StudyNote 모델 데이터 복사 및 StudyNoteContent 생성
                for original_pk in selectedRowPksFromOriginalTable:
                    original_study_note = StudyNote.objects.get(pk=original_pk)

                    # StudyNote 복사
                    new_study_note = StudyNote.objects.create(
                        title=original_study_note.title,
                        description=original_study_note.description,
                        writer=user
                    )

                    # StudyNoteContent 생성
                    original_note_contents = original_study_note.note_contents.all()
                    for original_note_content in original_note_contents:
                        StudyNoteContent.objects.create(
                            study_note=new_study_note,
                            title=original_note_content.title,
                            file_name=original_note_content.file_name,
                            content=original_note_content.content,
                            writer=user,
                            order=original_note_content.order,
                            created_at=original_note_content.created_at,
                            page=original_note_content.page
                        )

                response_data = {
                    'message': 'Selected notes copied to my note successfully.'
                }

                return Response(response_data, status=HTTP_200_OK)

            except StudyNote.DoesNotExist:
                response_data = {
                    'message': 'One or more selected notes do not exist.'
                }

                return Response(response_data, status=HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForCheckedRows(APIView):
    total_page_count = 0  # 노트의 총 개수

    def get(self, request):
        selected_row_pks = request.GET.get(
            "selectedRowPksFromOriginalTable", "").split(",")
        print("selected_row_pks :::::::::::::::::::", selected_row_pks)

        all_study_note_list = StudyNote.objects.filter(
            pk__in=selected_row_pks,
        )
        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list

        serializer = StudyNoteSerializer(study_notes, many=True)

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
        }

        return Response(response_data, status=HTTP_200_OK)


from django.db import transaction

class UpdateNoteContentsPageForSelectedView(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, study_note_pk):
        direction = request.data.get('direction')
        pageNumbersToEdit = request.data.get('pageNumbersToEdit') # 초록색
        pageNumbersToMove = request.data.get('pageNumbersToMove') # 주황색

        try:
            with transaction.atomic():
                study_note = self.get_object(study_note_pk)  # 특정 노트
                study_note_contents = study_note.note_contents.all()  # 모든 노트

                if direction == 'forward':
                    for content in study_note_contents:
                        if content.page in pageNumbersToEdit:
                            new_page = pageNumbersToMove[pageNumbersToEdit.index(content.page)]
                            content.page = new_page
                            content.created_at = timezone.now()
                            content.save()

                elif direction == 'backward':
                    for content in study_note_contents:
                        if content.page in pageNumbersToMove:
                            new_page = pageNumbersToEdit[pageNumbersToMove.index(content.page)]
                            content.page = new_page
                            content.save()

                elif direction == 'switch':
                    for edit_page, move_page in zip(pageNumbersToEdit, pageNumbersToMove):
                        edit_contents = study_note_contents.filter(page=edit_page)
                        move_contents = study_note_contents.filter(page=move_page)

                        if edit_contents.count() == move_contents.count() == 1:
                            edit_content = edit_contents.first()
                            move_content = move_contents.first()

                            edit_content.page, move_content.page = move_page, edit_page
                            edit_content.save()
                            move_content.save()

                elif direction == 'add_whitespace':
                    max_page = 0  # 초기값 설정

                    if pageNumbersToEdit:
                        max_page = max(max_page, max(pageNumbersToEdit))

                    # 공백 만들 페이지 이후의 번호를 a만큼 증가시킴
                    a = len(pageNumbersToEdit)
                    for content in study_note_contents:
                        if content.page > max_page:
                            content.page += a
                            content.save()

                    # pageNumbersToEdit의 페이지도 a만큼 증가시킴
                    for page_num in pageNumbersToEdit:
                        contents_to_update = study_note_contents.filter(page=page_num)
                        for content in contents_to_update:
                            content.page += a
                            content.save()

                elif direction == 'insert':
                    max_page = 0  # 초기값 설정

                    if pageNumbersToEdit:
                        max_page = max(max_page, max(pageNumbersToEdit))

                    # 모든 페이지 번호를 a만큼 증가시킴
                    a = len(pageNumbersToEdit)
                    for content in study_note_contents:
                        if content.page > max_page:
                            content.page += a
                            content.save()

                    # pageNumbersToEdit의 페이지도 a만큼 증가시킴
                    for page_num in pageNumbersToEdit:
                        contents_to_update = study_note_contents.filter(page=page_num)
                        for content in contents_to_update:
                            content.page += a
                            content.save()

                    # pageNumbersToMove 의 모든 요소들을 a 만큼 더함
                    pageNumbersToMove = [x + a for x in pageNumbersToMove] 

                    for content in study_note_contents:
                        if content.page in pageNumbersToMove:
                            new_page = pageNumbersToEdit[pageNumbersToMove.index(content.page)]
                            content.page = new_page
                            content.save()                    


                if direction == "forward":
                    message = f"{pageNumbersToEdit}를 pageNumbersToMove로 이동 성공"
                elif direction == "backward":
                    message = f"pageNumbersToMove를 {pageNumbersToEdit}로 이동 성공"
                elif direction == "switch":
                    message = f"{pageNumbersToEdit} <=> {pageNumbersToMove} 교체 성공"
                elif direction == "add_whitespace":
                    message = f"{pageNumbersToEdit} 공백 만들기 성공"
                elif direction == "insert":
                    message = f"공백 만들기 + 끼워 넣기 성공"

                response_data = {
                    "message": message,
                    "direction": direction,
                }

                return Response(data=response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(data={"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudyNoteContentReOrderAPIView(APIView):
    def put(self, request, pk):
        try:
            study_note_contents = StudyNoteContent.objects.filter(
                study_note__pk=pk)

            print("study_note_contents : ", study_note_contents)

            reordered_contents_list = request.data.get(
                'reordered_contents_list', [])
            print("reordered_contents_list : ", reordered_contents_list)

            for item in reordered_contents_list:
                pk_for_update = item['content_pk']
                order_for_update = item['order']

                print("pk_for_update, order_for_update : ",
                      pk_for_update, order_for_update)

                study_note_content = study_note_contents.get(
                    pk=pk_for_update)
                study_note_content.order = order_for_update
                study_note_content.save()

            study_note_contents = StudyNoteContent.objects.filter(
                study_note__pk=pk, page=1)

            print("study_note_contents : ", study_note_contents)

            # serializer = StudyNoteContentSerializer(study_note_content, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({'success': 'Study note content order updated successfully.'}, status=status.HTTP_200_OK)

        except StudyNoteContent.DoesNotExist:
            return Response({'error': 'Study note content does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class SearchContentListView(APIView):
    def get(self, request):
        study_note_pk = request.query_params.get('study_note_pk')
        search_term = request.query_params.get('searchTerm')

        print("search_term : ", search_term)

        # 필요한 로직 수행
        queryset = StudyNoteContent.objects.filter(study_note=study_note_pk)

        print("queryset : ", queryset)

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term)
            )
        print("queryset2 : ", queryset)

        serializer = StudyNoteContentSerializer(queryset, many=True)

        print("serializer.data : ", serializer.data)

        return Response(serializer.data)


class DeleteNoteContentsForChecked(APIView):
    def delete(self, request):
        username = request.data.get('username')  # 'username' 값 받기
        pageNumbersToEdit = request.data  # [1, 2, 3, 5]
        print("pageNumbersToEdit : ", pageNumbersToEdit)

        # username에 해당하는 User 객체 가져오기
        writer = User.objects.get(username=username)

        deleted_count = StudyNoteContent.objects.filter(
            writer=writer,
            pk__in=pageNumbersToEdit).delete()[0]

        return Response({
            'message': f'{deleted_count} StudyNoteContent instances deleted.'
        })


class order_plus_one_for_note_content(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, content_pk):
        # 해당하는 객체 찾기
        content = get_object_or_404(StudyNoteContent, pk=content_pk)

        # 먼저 +1 인거 -1 처리
        # order 값이 증가된 객체보다 큰 값을 가지는 다른 객체들의 order 값을 1씩 감소시키기
        other_content = StudyNoteContent.objects.get(
            study_note=content.study_note,
            order=content.order + 1
        )

        study_note = self.get_object(content.study_note.pk)
        note_contents_after_order_update = study_note.note_contents.filter(
            page=content.page).order_by('order')

        # order 값을 1 증가시키고 저장
        content.order += 1
        content.save()

        other_content.order -= 1
        other_content.save()

        serializer = StudyNoteContentSerializer(
            note_contents_after_order_update, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class order_minus_one_for_note_content(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, content_pk):
        # 해당하는 객체 찾기
        content = get_object_or_404(StudyNoteContent, pk=content_pk)

        # 먼저 +1 인거 -1 처리
        # order 값이 증가된 객체보다 큰 값을 가지는 다른 객체들의 order 값을 1씩 감소시키기
        other_content = StudyNoteContent.objects.get(
            study_note=content.study_note,
            order=content.order - 1
        )
        other_content.order += 1
        other_content.save()

        study_note = self.get_object(content.study_note.pk)
        note_contents_after_order_update = study_note.note_contents.filter(
            page=content.page).order_by('order')

        # order 값을 1 증가시키고 저장
        content.order -= 1
        content.save()

        serializer = StudyNoteContentSerializer(
            note_contents_after_order_update, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudyNoteContentView(APIView):
    def delete(self, request, content_pk):
        try:
            content = StudyNoteContent.objects.get(pk=content_pk)
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudyNoteContent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, content_pk, format=None):
        study_note_content = StudyNoteContent.objects.get(pk=content_pk)

        study_note_content.title = request.data.get(
            'title', study_note_content.title)
        study_note_content.file_name = request.data.get(
            'file_name', study_note_content.file_name)
        study_note_content.content = request.data.get(
            'content', study_note_content.content)

        study_note_content.save()

        return Response(status=status.HTTP_200_OK)

class StudyNoteContentsView(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        title = request.data["title"]
        file = request.data["file"]
        content = request.data["content"]
        content_option = request.data["content_option"]
        print("content_option : ", content_option)

        # 이전 order 값 중 최대값 구하기
        max_order = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, page=current_page_number).aggregate(Max('order'))['order__max'] or 0

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            title=title,
            file_name=file,
            content_option=content_option,
            content=content,
            writer=request.user,  # 작성자는 현재 요청한 유저로 설정
            page=current_page_number,
            order=max_order + 1,  # 이전 order 값 중 최대값에 1을 더하여 설정
        )
        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)

class CreteViewForFAQBoard(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        title = request.data["title"]
        content = request.data["content"]

        note_content = FAQBoard.objects.create(
            study_note_id=study_note_pk,
            title=title,
            content=content,
            writer=request.user
        )
        print("note_content : ", note_content)

        return Response(status=status.HTTP_201_CREATED)


class PlusOnePageForSelectedPageForStudyNoteContents(APIView):
    def put(self, request, study_note_pk):
        pageNumbersToEdit = request.data.get('pageNumbersToEdit', [])
        print("pageNumbersToEdit : ", pageNumbersToEdit)
        # pageNumbersToEdit 는 [1,2,3,5] 와 같이 리스트 형태로 넘어옵니다.

        # 선택된 StudyNote의 StudyNoteContent들의 page를 +1 해줍니다.
        study_note_contents = StudyNoteContent.objects.filter(
            study_note__pk=study_note_pk, page__in=pageNumbersToEdit)
        for study_note_content in study_note_contents:
            study_note_content.page += 1
            study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class MinusOnePageForSelectedPageForStudyNoteContents(APIView):
    def put(self, request, study_note_pk):
        pageNumbersToEdit = request.data.get('pageNumbersToEdit', [])
        print("pageNumbersToEdit : ", pageNumbersToEdit)
        # selected_buttons_data 는 [1,2,3,5] 와 같이 리스트 형태로 넘어옵니다.

        # 선택된 StudyNote의 StudyNoteContent들의 page를 +1 해줍니다.
        study_note_contents = StudyNoteContent.objects.filter(
            study_note__pk=study_note_pk, page__in=pageNumbersToEdit)
        for study_note_content in study_note_contents:
            study_note_content.page -= 1
            study_note_content.save()

        return Response(status=status.HTTP_200_OK)


class DeleteNoteContentsForSelectedPage(APIView):
    def delete(self, request, study_note_pk):
        selected_buttons_data = request.data

        StudyNoteContent.objects.filter(
            study_note_id=study_note_pk,
            page__in=selected_buttons_data
        ).delete()

        message = "노트에 대해  {} 페이지 삭제 완료".format(selected_buttons_data)

        return Response({'message': message})


class StudyNoteAPIView(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 4  # 1 페이지에 몇개씩

    def get(self, request):
        selected_note_writer = request.query_params.get(
            "selectedNoteWriter", "")
        first_category = request.query_params.get(
            "first_category", "")
        second_category = request.query_params.get(
            "second_category", "")

        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # study_notes 데이터중 start, end 에 해당하는 데이터 가져 오기
        if selected_note_writer == "" and first_category == "" and second_category == "":
            all_study_note_list = StudyNote.objects.all()
        else:
            filter_conditions = Q()
            if selected_note_writer != "":
                filter_conditions &= Q(writer__username=selected_note_writer)
            if first_category != "":
                filter_conditions &= Q(first_category=first_category)
            if second_category != "":
                filter_conditions &= Q(second_category=second_category)

            all_study_note_list = StudyNote.objects.filter(filter_conditions)

        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list[start:end]

        serializer = StudyNoteSerializer(study_notes, many=True)

        all_study_note_list_for_users = StudyNote.objects.all()
        note_writers = [
            note.writer.username for note in all_study_note_list_for_users]
        # Convert to set to remove duplicates, then convert back to list
        note_writers = list(set(note_writers))

        response_data = {
            "note_writers": note_writers,  # Include the note writers in the response
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page
        }

        return Response(response_data, status=HTTP_200_OK)

    def post(self, request):
        print("study note post 요청")
        serializer = StudyNoteSerializer(data=request.data)

        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            errors = serializer.errors
            print("serializer errors:", errors)  # 에러 출력
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print("put 요청 check !!")
        study_note_pk = request.data.get("study_note_pk")
        try:
            study_note = StudyNote.objects.get(pk=study_note_pk)
        except StudyNote.DoesNotExist:
            return Response({"error": "Study note does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudyNoteSerializer(study_note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForCopyMode(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 6  # 1 페이지에 몇개씩

    def get(self, request):
        selected_note_writer = request.query_params.get("selectedNoteWriter")

        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # study_notes 데이터중 start, end 에 해당하는 데이터 가져 오기

        if selected_note_writer == "":
            all_study_note_list = StudyNote.objects.filter(
                ~Q(writer__username=request.user.username))
        else:
            all_study_note_list = StudyNote.objects.filter(
                writer__username=selected_note_writer)
        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list[start:end]

        serializer = StudyNoteSerializer(study_notes, many=True)

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page
        }

        return Response(response_data, status=HTTP_200_OK)

    def post(self, request):
        serializer = StudyNoteSerializer(data=request.data)

        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudyNoteAPIViewForMe(APIView):
    total_page_count = 0  # 노트의 총 개수
    note_count_per_page = 6  # 1 페이지에 몇개씩

    def get(self, request):
        print("all_study_note_list for me check !!!!!!!!!!!!!")
        # step1 page 번호 가져 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 page 에 해당하는 데이터 가져 오기
        start = (page - 1) * self.note_count_per_page
        end = start + self.note_count_per_page

        # study_notes 데이터중 start, end 에 해당하는 데이터 가져 오기
        all_study_note_list = StudyNote.objects.filter(
            Q(writer__username=request.user.username))

        # print("all_study_note_list For Me :::::::::::::::::", all_study_note_list)

        self.total_page_count = len(all_study_note_list)
        study_notes = all_study_note_list[start:end]

        serializer = StudyNoteSerializer(study_notes, many=True)

        response_data = {
            "noteList": serializer.data,
            "totalPageCount": self.total_page_count,
            "note_count_per_page": self.note_count_per_page
        }

        return Response(response_data, status=HTTP_200_OK)

    def post(self, request):
        serializer = StudyNoteSerializer(data=request.data)
        print("request.user : ", request.user)

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class StudyNoteDetailView(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def get(self, request, notePk, pageNum):
        # study note 정보 가져 오기
        study_note = self.get_object(notePk)
        # current_page = request.GET.get('currentPage', 1)

        question_count_for_current_page = study_note.question_list.filter(
            page=pageNum).count()
        print("question_count_for_current_page ::::::::::::::::::::::::::::::::::::::::",
              question_count_for_current_page)

        print("current_page : ", pageNum)
        note_contents = study_note.note_contents.filter(
            page=pageNum).order_by('order')

        filtered_contents = note_contents.filter(
            content_option="subtitle_for_page")

        if filtered_contents.exists():
            subtitle_for_page = filtered_contents[0].title
        else:
            subtitle_for_page = "no data"

        serializer = StudyNoteContentSerializer(note_contents, many=True)
        data = serializer.data

        total_note_contents = study_note.note_contents.all().order_by('order')
        # print("total_note_contents :::::::::::::::::::: ", total_note_contents)

        page_numbers = total_note_contents.values(
            'page').annotate(count=Count('id')).order_by('page')
        # print("page_numbers :::::::::::::::::", page_numbers)
        exist_page_numbers = [page['page'] for page in page_numbers]
        # print("exist_page_numbers ::::::::::::::: ", exist_page_numbers)

        # todo
        # study_note.note_cowriters를 가져와 cowriters에 담은 뒤 response_data에 추가
        cowriters = study_note.note_cowriters.all()
        cowriters_data = []
        for cowriter in cowriters:
            if cowriter.is_approved:
                # # cowriters_data.append(cowriter.writer.username)
                cowriter_data = {
                    "username": cowriter.writer.username,
                    "profile_image": cowriter.writer.profile_image
                }
                cowriters_data.append(cowriter_data)

        response_data = {
            "note_title": study_note.title,
            "subtitle_for_page": subtitle_for_page,
            "note_user_name": study_note.writer.username,
            "note_user_profile_image": study_note.writer.profile_image,
            "exist_page_numbers": exist_page_numbers,
            "data_for_study_note_contents": data,
            "co_writers_for_approved": cowriters_data,
            "question_count_for_current_page": question_count_for_current_page
        }

        return Response(response_data, status=HTTP_200_OK)


class AddDummyDataForStudyNote(APIView):
    def post(self, request):
        for i in range(10):
            title = f"Dummy Note {i+1}"
            description = f"This is a dummy note with index {i+1}"
            StudyNote.objects.create(title=title, description=description)
        return Response({"message": "Dummy data added successfully."})


class StudyNoteContentDummyAPI(APIView):
    def post(self, request):
        study_notes = StudyNote.objects.all()
        print("study_notes :", study_notes)

        for i in range(5):
            study_note_obj = random.choice(study_notes)

            if study_note_obj:
                StudyNoteContent.objects.create(
                    title=f"dummy title {i}",
                    content=f"dummy content {i}",
                    writer=request.user,
                    study_note=study_note_obj,
                    # created_at=datetime.now() - timedelta(days=i),
                )
        return Response({"message": "Dummy data created successfully."})
