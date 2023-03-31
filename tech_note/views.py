from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated

from .models import TechNote, TechNoteContent
from .serializers import CreateTechNoteSerializer, TechNoteSerializer


@csrf_exempt
def create_dummy_tech_notes(request):
    for i in range(50):
        note = TechNote.objects.create(
            title=f"Dummy Note {i}",
            category=TechNote.CATEGORY_CHOICES.create,
        )
    return JsonResponse({"message": "Dummy notes created successfully."})


class UpdateLikeView(APIView):
    def get_object(self, pk):
        try:
            return TechNote.objects.get(pk=pk)
        except TechNote.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        tech_note = self.get_object(pk)

        if tech_note:
            before_like_count = tech_note.like_count
            tech_note.like_count += 1
        else:
            raise ParseError(pk+"에 해당하는 노트가 없습니다")

        tech_note.save()

        result_data = {
            "success": True,
            "message": f'start point update success from {before_like_count} to {before_like_count+1} '
        }

        return Response(result_data, status=HTTP_200_OK)


class TechNotes(APIView):
    # step1 클래스 변수 선언 , total_count_for_tech_note_table_rows = 테이블 모든 행의 개수
    total_count_for_tech_note_table_rows = 0
    number_for_one_page = 10

    def get(self, request):
        # step2 default page num = 1 로 설정
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step3 all list 가져오기
        all_tech_notes = TechNote.objects.all().order_by("-created_at")
        self.total_count_for_tech_note_table_rows = all_tech_notes.count()
        # step4 페이지 번호와 연동 되는 start 와 end 설정 <=> ex) all_tech_notes[0:5] 01234
        # (1 - 1 * 5 ~  0  + 5) => 0 ~ 5 <=> 1페이지 일때
        # (2 - 1 * 5 ~  5 + 5) => 5 ~ 10 <=> 2페이지 일때
        # (3 - 1 * 5 ~  10 + 5) => 10 ~ 15 <=> 3페이지 일때
        start = (page - 1) * self.number_for_one_page
        end = start + self.number_for_one_page

        # step5 start end 에 해당 하는 목록 가져 오기
        tech_notes_for_page = all_tech_notes[start:end]

        serializer = TechNoteSerializer(tech_notes_for_page, many=True)

        data = {
            "total_count_for_tech_note_table_rows": self.total_count_for_tech_note_table_rows,
            "tech_note_list_for_page": serializer.data
        }

        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        print("request.data : ", request.data)
        print("request.data['title] : ", request.data['title'])
        print("request.data['category] : ", request.data['category'])

        serializer = CreateTechNoteSerializer(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                tech_note = serializer.save()
                serializer = TechNoteSerializer(tech_note)
                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")

    # 넘어올 데이터: techNotePk,category_option,tech_note_description,

    def put(self, request):

        techNotePk = request.data.get("techNotePk")
        tech_note_description = request.data.get("tech_note_description")
        category_option = request.data.get("category_option")

        print("techNotePk : ", techNotePk)
        print("tech_note_description : ", tech_note_description)
        print("category_option : ", category_option)

        tech_note = TechNote.objects.get(pk=techNotePk)

        # 업데이트 할것 title, category
        tech_note.title = tech_note_description
        tech_note.category = category_option
        tech_note.save()

        result_data = {
            "success": True,
            "message": "tech_note update success"
        }

        return Response(result_data, status=HTTP_200_OK)


class TechNoteListDeleteView(APIView):

    def get_object(self, taskPk):
        try:
            return TechNote.objects.get(pk=taskPk)
        except TechNote.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        print("삭제 요청 확인 for pk : ", pk)
        try:
            tech_note = self.get_object(pk)
            tech_note.delete()
        except Exception as e:
            raise ParseError(f"삭제 요청 에러입니다: {str(e)}")

        return Response(status=HTTP_204_NO_CONTENT)


class TechNoteContentView(APIView):
    def get_object(self, pk):
        try:
            return TechNote.objects.get(pk=pk)
        except TechNote.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        tech_note = self.get_object(pk)
        print("tech_note : ", tech_note)
        tech_note_contents = TechNoteContent.objects.filter(tech_note=tech_note)
        print("tech_note_contents : ", tech_note_contents)

        return Response({"success": "true"})
