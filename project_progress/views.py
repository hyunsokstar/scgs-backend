import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProjectProgress
from project_progress.serializers import CreateProjectProgressSerializer, ProjectProgressListSerializer
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated


class ProjectProgressView(APIView):
    totalCount = 0  # total_count 계산
    total_page_count = 10  # 1 페이지에 몇개씩

    def get(self, request):
        # step2 query 파라미터에서 page 가져오기 or 1
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        all_project_progresses = ProjectProgress.objects.all()
        serializer = ProjectProgressListSerializer(
            all_project_progresses, many=True)

        # step3 해당 페이지(쿼리 파라미터로 페이지 넘버 얻어옴)에 대한 리스트 정보 가져온뒤 직렬화
        page_size = self.total_page_count
        total_page_count = self.totalCount
        start = (page - 1) * page_size
        end = start + page_size
        all_estimate_requires = ProjectProgress.objects.all()[start:end]

        serializer = ProjectProgressListSerializer(
            all_estimate_requires, many=True)
        
        # 총 페이지 숫자 계산
        if (ProjectProgress.objects.all().count() % 3 == 0):
            total_page_count = ProjectProgress.objects.all().count()/page_size
        else:
            total_page_count = ProjectProgress.objects.all().count()/page_size + 1

        total_page_count = math.trunc(total_page_count)        

        # step5 응답
        data = serializer.data
        data = {"totalPageCount": total_page_count, "ProjectProgressList": data}
        return Response(data, status=HTTP_200_OK)
    
    def post(self, request):
        serializer = CreateProjectProgressSerializer(data=request.data)
        if serializer.is_valid():
            project_progress = serializer.save()
            return Response(CreateProjectProgressSerializer(project_progress).data)
        else:
            print("serializer.errors : " ,serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)


class ProjectProgressDetailView(APIView):
    pass

# ProjectProgress 모델에 대해 pk 에 해당하는 completed 를 이전과 반대로 update
class UpdateTaskCompetedView(APIView):

    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""     
        print("put 요청 확인")
        project_task = self.get_object(pk)

        if project_task.task_completed:
            message = "완료에서 비완료로 update"
            project_task.task_completed = False
        else:
            message = "비완료에서 완료로 update"
            project_task.task_completed = True

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)
    

class UpdateProjectTaskImportance(APIView):

    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("put 요청 확인")

        # request body 에서 star_count 가져 오기
        star_count = request.data.get("star_count")

        # 해당 행 찾기
        project_task = self.get_object(pk)
        before_star_count = project_task.importance

        # 업데이트할 값 설정 후 save()
        project_task.importance = star_count
        project_task.save()

        result_data = {
            "success": True,
            "message": f'start point update success from {before_star_count} to {star_count} '
        }

        return Response(result_data, status=HTTP_200_OK)
      