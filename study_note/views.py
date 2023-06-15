from django.db import transaction
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CoWriterForStudyNote, StudyNote, StudyNoteContent
from .serializers import StudyNoteContentSerializer, StudyNoteSerializer
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
from .models import StudyNoteContent
from .serializers import StudyNoteContentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min
from django.db import models


class CreateViewForSubTitleForNote(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        content_option = request.data["content_option"]
        title = request.data["title"]
        ref_url1 = request.data["ref_url1"]
        ref_url2 = request.data["ref_url2"]
        content = request.data["content"]

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

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            page=current_page_number,
            content_option=content_option,
            writer=request.user,  # 작성자는 현재 요청한 유저로 설정
            # order=max_order + 1,  # 이전 order 값 중 최대값에 1을 더하여 설정
            order=order_for_update,  # 이전 order 값 중 최대값에 1을 더하여 설정
            title=title,
            ref_url1=ref_url1,
            ref_url2=ref_url2,
            content=content
        )

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


class UpdateNoteContentsPageForSelectedView(APIView):
    def get_object(self, pk):
        try:
            return StudyNote.objects.get(pk=pk)
        except StudyNote.DoesNotExist:
            raise NotFound

    def put(self, request, study_note_pk):
        direction = request.data.get('direction')
        pageNumbersToEdit = request.data.get('pageNumbersToEdit')
        pageNumbersToMove = request.data.get('pageNumbersToMove')

        # 데이터 출력
        print("----- API 데이터 -----\n")
        print(f"Direction: {direction}")
        print(f"Study Note PK: {study_note_pk}")
        print(f"Page Numbers to Edit: {pageNumbersToEdit}")
        print(f"Page Numbers to Move: {pageNumbersToMove}")
        print("\n----------------------")

        study_note = self.get_object(study_note_pk)
        study_note_contents = study_note.note_contents.all()
        # todo1
        # direction: forward 이라면
        #
        # pageNumbersToEdit: [1, 2]
        # pageNumbersToMove: [3, 4]
        # 에 대해

        # 이때 study_note_contents 가 1인것은 3으로 2인것은 4로 바꾸기

        # direction: backward 이라면
        #
        # pageNumbersToEdit: [1, 2]
        # pageNumbersToMove: [3, 4]
        # 에 대해
        # 이때 study_note_contents 가 3인것은 1으로 4인것은 2로 바꾸기

        # step1 일단 노트 내용 다 가져 오기
        study_note = self.get_object(study_note_pk)
        study_note_contents = study_note.note_contents.all()

        if direction == 'forward':
            # todo1: study_note_contents의 page 번호가 pageNumbersToEdit에 포함되어 있는 경우
            # 설명 pageNumbersToEdit.index(content.page) <=> content.page 에 해당하는 값이 있을 경우 index 를 구해라
            # 해당 page 번호를 pageNumbersToMove와 동일한 인덱스의 값으로 업데이트
            for content in study_note_contents:
                if content.page in pageNumbersToEdit:
                    new_page = pageNumbersToMove[pageNumbersToEdit.index(
                        content.page)]
                    content.page = new_page
                    content.save()

        elif direction == 'backward':
            # todo2: study_note_contents의 page 번호가 pageNumbersToMove에 포함되어 있는 경우
            # 해당 page 번호를 pageNumbersToEdit와 동일한 인덱스의 값으로 업데이트
            for content in study_note_contents:
                if content.page in pageNumbersToMove:
                    new_page = pageNumbersToEdit[pageNumbersToMove.index(
                        content.page)]
                    content.page = new_page
                    content.save()

        # elif direction == 'switch':
            # todo3
            # pageNumbersToEdit: [1, 2] , pageNumbersToMove: [3, 4] 일 경우 1 과 3을 교체 2와 4를 교체, 즉 인덱스가 같은 것들을 교체
            # 즉 for content in study_note_contents: 에서 content.page 가 1인것들은 contet.page 를 3으로 3이었던것들은 1로

        elif direction == 'switch':
            # todo3
            # pageNumbersToEdit: [1, 2] , pageNumbersToMove: [3, 4] 일 경우 1 과 3을 교체 2와 4를 교체, 즉 인덱스가 같은 것들을 교체
            # 즉 for content in study_note_contents: 에서 content.page 가 1인것들은 contet.page 를 3으로 3이었던것들은 1로

            # 인덱스가 같은 요소들을 교체하기 위해 zip 함수를 사용하여 pageNumbersToEdit와 pageNumbersToMove를 묶습니다.
            for edit_page, move_page in zip(pageNumbersToEdit, pageNumbersToMove):
                # page 번호가 edit_page인 study_note_contents를 찾습니다.
                edit_contents = study_note_contents.filter(page=edit_page)
                # page 번호가 move_page인 study_note_contents를 찾습니다.
                move_contents = study_note_contents.filter(page=move_page)

                # edit_contents와 move_contents의 개수가 같고, 모두 존재할 경우에만 교체를 수행합니다.
                if edit_contents.count() == move_contents.count() == 1:

                    # save 하기 위한 객체를 각각 초기화
                    edit_content = edit_contents.first()
                    move_content = move_contents.first()

                    # page 번호를 교체합니다.
                    edit_content.page, move_content.page = move_page, edit_page
                    edit_content.save()
                    move_content.save()

        if direction == "forward":
            message = f"{pageNumbersToEdit}를 pageNumbersToMove로 이동 성공"
        elif direction == "backward":
            message = f"pageNumbersToMove를 {pageNumbersToEdit}로 이동 성공"
        elif direction == "switch":
            message = f"{pageNumbersToEdit} <=> {pageNumbersToMove} 교체 성공"

        response_data = {
            "message": message,
            "direction": direction,
        }

        # HTTP 200 OK 응답 반환
        return Response(data=response_data, status=status.HTTP_200_OK)


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
    note_count_per_page = 6  # 1 페이지에 몇개씩

    def get(self, request):
        selected_note_writer = request.query_params.get(
            "selectedNoteWriter", "")

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
            all_study_note_list = StudyNote.objects.all()
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

    def get(self, request, notePk):
        # study note 정보 가져 오기
        study_note = self.get_object(notePk)
        current_page = request.GET.get('currentPage', 1)
        print("current_page : ", current_page)
        note_contents = study_note.note_contents.filter(
            page=current_page).order_by('order')

        serializer = StudyNoteContentSerializer(note_contents, many=True)
        data = serializer.data

        total_note_contents = study_note.note_contents.all().order_by('order')
        print("total_note_contents :::::::::::::::::::: ", total_note_contents)

        page_numbers = total_note_contents.values(
            'page').annotate(count=Count('id')).order_by('page')
        print("page_numbers :::::::::::::::::", page_numbers)
        exist_page_numbers = [page['page'] for page in page_numbers]
        print("exist_page_numbers ::::::::::::::: ", exist_page_numbers)

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
            "note_user_name": study_note.writer.username,
            "exist_page_numbers": exist_page_numbers,
            "data_for_study_note_contents": data,
            "co_writers_for_approved": cowriters_data
        }

        return Response(response_data, status=HTTP_200_OK)

    # def get(self, request, pk):
    #     page_count = StudyNoteContent.objects.values('page').annotate(count=Count('id')).order_by('page')
    #     result = [page['page'] for page in page_count]
    #     return Response(result)

    def delete(self, request, pk):
        api_docu = self.get_object(pk)
        api_docu.delete()

        return Response(status=HTTP_204_NO_CONTENT)


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
