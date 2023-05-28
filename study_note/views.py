from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudyNote, StudyNoteContent
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
from django.db.models import Q

# 1122
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import StudyNoteContent
from .serializers import StudyNoteContentSerializer

# 
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
        study_note = self.get_object(study_note_pk)
        study_note_contents = study_note.note_contents.all()

        if direction == 'forward':
            # todo1: study_note_contents의 page 번호가 pageNumbersToEdit에 포함되어 있는 경우
            # 해당 page 번호를 pageNumbersToMove와 동일한 인덱스의 값으로 업데이트
            for content in study_note_contents:
                if content.page in pageNumbersToEdit:
                    new_page = pageNumbersToMove[pageNumbersToEdit.index(content.page)]
                    content.page = new_page
                    content.save()

        elif direction == 'backward':
            # todo2: study_note_contents의 page 번호가 pageNumbersToMove에 포함되어 있는 경우
            # 해당 page 번호를 pageNumbersToEdit와 동일한 인덱스의 값으로 업데이트
            for content in study_note_contents:
                if content.page in pageNumbersToMove:
                    new_page = pageNumbersToEdit[pageNumbersToMove.index(content.page)]
                    content.page = new_page
                    content.save()

        if direction == "forward":
            message = f"{pageNumbersToEdit}를 pageNumbersToMove로 이동 성공"
        elif direction == "backward":
            message = f"pageNumbersToMove를 {pageNumbersToEdit}로 이동 성공"

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

                print("pk_for_update, order_for_update : ", pk_for_update, order_for_update)

                study_note_content =  study_note_contents.get(
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
        pageNumbersToEdit = request.data  # [1, 2, 3, 5]
        print("pageNumbersToEdit : ", pageNumbersToEdit)

        deleted_count = StudyNoteContent.objects.filter(
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
        
        study_note_content.title = request.data.get('title', study_note_content.title)
        study_note_content.file_name = request.data.get('file_name', study_note_content.file_name)
        study_note_content.content = request.data.get('content', study_note_content.content)
        
        study_note_content.save()
        
        return Response(status=status.HTTP_200_OK)

class StudyNoteContentsView(APIView):
    def post(self, request, study_note_pk):
        study_note_pk = int(study_note_pk)
        current_page_number = int(request.data["current_page_number"])
        title = request.data["title"]
        file = request.data["file"]
        content = request.data["content"]

        # 이전 order 값 중 최대값 구하기
        max_order = StudyNoteContent.objects.filter(
            study_note_id=study_note_pk, page=current_page_number).aggregate(Max('order'))['order__max'] or 0

        # StudyNoteContent 모델 생성
        note_content = StudyNoteContent.objects.create(
            study_note_id=study_note_pk,
            title=title,
            file_name=file,
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
    def get(self, request):
        study_notes = StudyNote.objects.all()
        serializer = StudyNoteSerializer(study_notes, many=True)
        return Response(serializer.data)

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

    def get(self, request, pk):
        study_note = self.get_object(pk)
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

        response_data = {
            "exist_page_numbers": exist_page_numbers,
            "data_for_study_note_contents": data,
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
