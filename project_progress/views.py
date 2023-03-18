import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProjectProgress
from project_progress.serializers import CreateProjectProgressSerializer, ProjectProgressDetailSerializer, ProjectProgressListSerializer
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated

# view 추가


class UncompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 5  # 1 페이지에 몇개씩

    def get(self, request):
        print("uncompleted task 요청 check !!")

        # step2 query 파라미터에서 page 가져오기 or 1
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        all_uncompleted_project_task_list = ProjectProgress.objects.filter(
            task_completed=False)
        count_for_all_uncompleted_project_task_list = ProjectProgress.objects.filter(
            task_completed=False).count()

        # 비완료 총개수
        print("count_for_all_uncompleted_project_task_list : ",
              count_for_all_uncompleted_project_task_list)

        # step3 해당 페이지(쿼리 파라미터로 페이지 넘버 얻어옴)에 대한 리스트 정보 가져온뒤 직렬화
        # self.task_number_for_one_page

        # total_page_count = self.totalCount

        # 알고리즘 설명 task_number_for_one_page 이 5 즉 한페이지당 5개씩 보여줄 경우 1페이지에 보여줄 list 의 start 와 end는
        # list[0~5] 이면 되는데 start end 의 패턴을 보면
        # (1 - 1 * 5 ~  0  + 5) => 0 ~ 5
        # (2 - 1 * 5 ~  5 + 5) => 5 ~ 10
        # (3 - 1 * 5 ~  10 + 5) => 10 ~ 15
        #  여기서 1-2-3 이 start
        #  뒤의 0  + 5 5 +5 end = start + page num 으로 하고
        # url query 파라 미터로 페이지번호만 전달해 주면
        #  아래와 같이 ProjectProgress.objects.filter(task_completed=False)[start:end] 으로 list 를 가져올 수 있게 됨
        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page
        uncompleted_project_task_list_for_current_page = all_uncompleted_project_task_list[
            start:end]

        serializer = ProjectProgressListSerializer(
            uncompleted_project_task_list_for_current_page, many=True)

        # 총 페이지 숫자 계산
        # if (count_for_all_completed_project_task_list % self.task_number_for_one_page == 0):
        #     self.totalCountForTask = count_for_all_completed_project_task_list 
        # else:
        #     self.totalCountForTask = count_for_all_completed_project_task_list + 1  

        self.totalCountForTask = math.trunc(count_for_all_uncompleted_project_task_list)

        # step5 응답
        data = serializer.data
        data = {
            "totalPageCount": self.totalCountForTask,
            "ProjectProgressList": data
        }
        return Response(data, status=HTTP_200_OK)

class CompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 5  # 1 페이지에 몇개씩

    def get(self, request):
        print("uncompleted task 요청 check !!")

        # step2 query 파라미터에서 page 가져오기 or 1
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        all_completed_project_task_list = ProjectProgress.objects.filter(
            task_completed=True)
        count_for_all_completed_project_task_list = ProjectProgress.objects.filter(
            task_completed=True).count()

        # 완료 총개수
        print("count_for_all_completed_project_task_list : ",
              count_for_all_completed_project_task_list)

        # step3 해당 페이지(쿼리 파라미터로 페이지 넘버 얻어옴)에 대한 리스트 정보 가져온뒤 직렬화
        # self.task_number_for_one_page

        # total_page_count = self.totalCount

        # 알고리즘 설명 task_number_for_one_page 이 5 즉 한페이지당 5개씩 보여줄 경우 1페이지에 보여줄 list 의 start 와 end는
        # list[0~5] 이면 되는데 start end 의 패턴을 보면
        # (1 - 1 * 5 ~  0  + 5) => 0 ~ 5
        # (2 - 1 * 5 ~  5 + 5) => 5 ~ 10
        # (3 - 1 * 5 ~  10 + 5) => 10 ~ 15
        #  여기서 1-2-3 이 start
        #  뒤의 0  + 5 5 +5 end = start + page num 으로 하고
        # url query 파라 미터로 페이지번호만 전달해 주면
        #  아래와 같이 ProjectProgress.objects.filter(task_completed=False)[start:end] 으로 list 를 가져올 수 있게 됨
        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page
        completed_project_task_list_for_current_page = all_completed_project_task_list[
            start:end]

        serializer = ProjectProgressListSerializer(
            completed_project_task_list_for_current_page, many=True)

        # 총 페이지 숫자 계산
        # if (count_for_all_completed_project_task_list % self.task_number_for_one_page == 0):
        #     self.totalCountForTask = count_for_all_completed_project_task_list 
        # else:
        #     self.totalCountForTask = count_for_all_completed_project_task_list + 1  

        self.totalCountForTask = math.trunc(count_for_all_completed_project_task_list)

        # step5 응답
        data = serializer.data
        data = {
            "totalPageCount": self.totalCountForTask,
            "ProjectProgressList": data
        }
        return Response(data, status=HTTP_200_OK)


class ProjectProgressDetailView(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        print("견적 디테일 페이지 요청 확인 (백엔드) !")
        print(pk, type(pk))

        project_task = self.get_object(pk)
        print("project_task : ", project_task)

        serializer = ProjectProgressDetailSerializer(
            project_task, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        print("request.data", request.data)
        print("pk : ", pk)

        project_task = self.get_object(pk)
        print("project_task : ", project_task)

        serializer = ProjectProgressDetailSerializer(
            project_task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                project_task = serializer.save()
                serializer = ProjectProgressDetailSerializer(project_task)
                return Response(serializer.data)

            except Exception as e:
                print("ee : ", e)
                raise ParseError("project_task not found")
        else:
            print("시리얼 라이저가 유효하지 않음")
            error_message = "serializer is not valid: {}".format(
                serializer.errors)
            ParseError("serializer is not valid: {}".format(serializer.errors))
            print(error_message)

    def delete(self, request, pk):
        print("삭제 요청 확인")
        project_task = self.get_object(pk)
        project_task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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
        data = {"totalPageCount": total_page_count,
                "ProjectProgressList": data}
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        serializer = CreateProjectProgressSerializer(data=request.data)
        if serializer.is_valid():
            project_progress = serializer.save()
            return Response(CreateProjectProgressSerializer(project_progress).data)
        else:
            print("serializer.errors : ", serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)


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
