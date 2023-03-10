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