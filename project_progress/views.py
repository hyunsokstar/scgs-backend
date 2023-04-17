import math
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from project_progress.serializers import CreateCommentSerializerForTask, CreateExtraTaskSerializer, CreateProjectProgressSerializer, CreateTestSerializerForOneTask, ProjectProgressDetailSerializer, ProjectProgressListSerializer, TestSerializerForOneTask, TestersForTestSerializer
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ProjectProgress, ExtraTask, TaskComment, TestForTask, TestersForTest
from django.db.models import Count
from users.serializers import UserProfileImageSerializer


class TaskStaticsIView(APIView):
    def get(self, request):
        task_managers = ProjectProgress.objects.values_list(
            'task_manager', flat=True).distinct()

        response_data = []
        for manager in task_managers:
            completed_count_for_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=True).count()
            count_for_testing_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=False, is_testing=True).count()
            uncompleted_count_for_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=False, is_testing=False).count()
            total_count_for_uncompleted_task = uncompleted_count_for_task + count_for_testing_task
            total_count_for_completed_task = uncompleted_count_for_task + \
                count_for_testing_task + completed_count_for_task
            task_manager = User.objects.get(pk=manager).username

            manager_data = {
                "task_manager": task_manager,
                "completed_count_for_task": completed_count_for_task,
                "count_for_testing_task": count_for_testing_task,
                "uncompleted_count_for_task": uncompleted_count_for_task,
                "total_count_for_uncompleted_task": total_count_for_uncompleted_task,
                "total_count_for_completed_task": total_count_for_completed_task
            }
            response_data.append(manager_data)

        return Response(response_data)


def get_writers_info(complete_status):
    print("complete_status2 : ", complete_status)
    task_manager_counts = ProjectProgress.objects.filter(task_completed=complete_status).values(
        'task_manager__username', 'task_manager__profile_image').annotate(count=Count('id'))
    print("task_manager_counts : ", task_manager_counts)

    task_managers_info = []
    for task_manager_count in task_manager_counts:
        writer_info = {
            "username": task_manager_count['task_manager__username'],
            "profile_image": task_manager_count['task_manager__profile_image'],
            "task_count": task_manager_count['count']
        }
        task_managers_info.append(writer_info)

    # result_data = {
        # "writersInfo": task_managers_info
    # }

    return task_managers_info


class TaskMangerInfo(APIView):
    def get(self, request):
        result_data = get_writers_info(complete_status=False)

        return Response(result_data)


class CommentForTaskView(APIView):
    def get_object(self, pk):
        try:
            return TaskComment.objects.get(pk=pk)
        except TaskComment.DoesNotExist:
            raise NotFound

    def delete(self, request, commentPk):
        comment_obj = self.get_object(commentPk)
        comment_obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class UpdateViewForCommentText(APIView):
    def get_object(self, pk):
        try:
            return TaskComment.objects.get(pk=pk)
        except TaskComment.DoesNotExist:
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


class UpdateViewForCommentEdit(APIView):
    def get_object(self, pk):
        try:
            return TaskComment.objects.get(pk=pk)
        except TaskComment.DoesNotExist:
            raise NotFound

    def put(self, request, commentPk):
        print("put 요청 확인")
        message = ""
        comment = self.get_object(commentPk)

        if comment.is_edit_mode:
            comment.is_edit_mode = False
            message = "edit mode to read mode"
            # project_task.completed_at = None  # completed_at을 blank 상태로 만듦

        else:
            comment.is_edit_mode = True
            message = "from read mode to edit mode"
            # new_completed_at = timezone.localtime()

        comment.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class ProjectProgressCommentView(APIView):
    def get_object(self, taskPk):
        try:
            return ProjectProgress.objects.get(pk=taskPk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def post(self, request, taskPk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = CreateCommentSerializerForTask(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                # original_task = self.get_object(taskPk)S
                test_for_task = serializer.save(writer=request.user)
                serializer = CreateExtraTaskSerializer(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")


class UpatedTestPassedForTasksView(APIView):
    def get_object(self, pk):
        try:
            return TestForTask.objects.get(pk=pk)
        except TestForTask.DoesNotExist:
            raise NotFound

    def put(self, request, testPk):
        message = ""
        print("put 요청 확인 : pk ", testPk)
        test_for_task = self.get_object(testPk)

        if test_for_task.test_passed:
            message = "test passed to 취소 !"
            test_for_task.test_passed = False
        else:
            message = "test_passed to success!"
            test_for_task.test_passed = True

        test_for_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)

# testers_for_test
# task tester created_at


class UpatedTestersForTestPkView(APIView):

    # def get_object(self, request, pk):
    #     try:
    #         return TestersForTest.objects.get(test=pk, tester=request.user)
    #     except TestersForTest.DoesNotExist:
    #         print("TestersForTest 에서 못찾았습니다.")
    #         raise NotFound

    def put(self, request, testPk):
        message = ""
        print("put 요청 확인 : pk ", testPk)

        if not request.user.is_authenticated:
            raise NotAuthenticated

        is_tester_aready_exists = TestersForTest.objects.filter(
            test=testPk, tester=request.user).exists()

        if is_tester_aready_exists == False:
            test = TestForTask.objects.get(pk=testPk)
            new_tester_for_test = TestersForTest(
                test=test, tester=request.user)
            new_tester_for_test.save()
            message = "test check success"

        else:
            TestersForTest.objects.filter(
                test=testPk).delete()
            message = "test check cancle !"

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class DeleteTestForTasksView(APIView):
    def get_object(self, taskPk):
        try:
            return TestForTask.objects.get(pk=taskPk)
        except TestForTask.DoesNotExist:
            raise NotFound

    def delete(self, request, testPk):
        print("삭제 요청 확인")
        test_for_task = self.get_object(testPk)
        test_for_task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class TestForTasks(APIView):
    def get_object(self, taskPk):
        try:
            return ProjectProgress.objects.get(pk=taskPk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def get(self, request, taskPk):
        print("pk(taskPk) : ", taskPk)
        original_task = self.get_object(taskPk)

        tests_for_original_task = original_task.tests_for_tasks.all()
        print("tests_for_original_task : ", tests_for_original_task)

        original_task_serializer = TestSerializerForOneTask(
            tests_for_original_task, many=True)

        return Response(original_task_serializer.data, status=HTTP_200_OK)

    def post(self, request, taskPk):

        serializer = CreateTestSerializerForOneTask(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                original_task = self.get_object(taskPk)
                test_for_task = serializer.save(original_task=original_task)
                serializer = CreateExtraTaskSerializer(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")


class UpdateExtraTaskImportance(APIView):
    def get_object(self, pk):
        try:
            return ExtraTask.objects.get(pk=pk)
        except ExtraTask.DoesNotExist:
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


class ExtraTasks(APIView):
    def get_object(self, pk):
        try:
            print("pk check at get_object : ", pk)
            return ExtraTask.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def post(self, request):
        print("request.data : ", request.data)
        print("request.data['task_manager] : ", request.data['task_manager'])

        serializer = CreateExtraTaskSerializer(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                userPk = request.data['task_manager']
                taskPk = request.data['taskPk']

                # print("userPk : ", userPk)
                # print("taskPk : ", taskPk)

                task_manager = User.objects.get(pk=userPk)
                original_task_obj = ProjectProgress.objects.get(pk=taskPk)
                extra_task = serializer.save(
                    original_task=original_task_obj, task_manager=task_manager)
                serializer = CreateExtraTaskSerializer(extra_task)
                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")

    def delete(self, request, pk):
        print("삭제 요청 확인 for pk : ", pk)
        try:
            extra_task = self.get_object(pk)
            extra_task.delete()
        except Exception as e:
            raise ParseError(f"삭제 요청 에러입니다: {str(e)}")

        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        print("hyunsok is king")
        print("put 요청 확인 : pk ", pk)
        extra_task = self.get_object(pk)
        task_status_before_update = extra_task.task_status
        task_status_for_update = request.data.get("task_status")

        extra_task.task_status = task_status_for_update
        if task_status_for_update == "in_progress":
            extra_task.started_at = timezone.now()
        if task_status_for_update == "ready":
            extra_task.started_at = None

        extra_task.save()

        result_data = {
            "success": True,
            "message": f'start point update success from {task_status_before_update} to {task_status_for_update} '
        }

        return Response(result_data, status=HTTP_200_OK)

# 0414


class TaskStatusListView(APIView):
    #   dateRange(string, default="thisMonth"),
    #   taskManagerForFiltering(number, default=""),
    #   importance(number, default=1),
    #   isRequestedForHelp(boolean, default=False),
    #   isBountyTask(boolean, default=False),
    #   dateRange = request.data.get("dateRange")
    one_month_ago = timezone.now() - timedelta(days=30)
    date_from = ""
    all_tasks = ProjectProgress.objects.all()

    def get_all_tasks(self, request):

        date_range = request.query_params.get('dateRange', 'thisMonth')
        task_manager = request.query_params.get(
            'taskManagerForFiltering', 'no_manager')
        importance = request.query_params.get('importance', 1)
        # is_requested_for_help = request.query_params.get('isRequestedForHelp', False)
        # is_bounty_task = request.query_params.get('isBountyTask', False)

        print("date_range, task_manager, importance : ",
              date_range, task_manager, importance)

        if (task_manager != ""):
            task_manager = User.objects.get(pk=task_manager)

        if (date_range == "thisMonth"):
            self.date_from = timezone.now() - timedelta(days=30)
        elif (date_range == "thisWeek"):
            self.date_from = timezone.now() - timedelta(days=7)
        elif (date_range == "today"):
            self.date_from = timezone.now() - timedelta(days=1)
        else:
            self.date_from = timezone.now() - timedelta(days=60)

        if (task_manager == ""):
            print("no manager !!!!!!!!!!!!!!!!!! :", task_manager)
            self.all_tasks = self.all_tasks.filter(
                created_at__gte=self.date_from, importance__gte=importance
            )
        else:
            print("manager is exist !!!!!!!!!!!!! : ", task_manager)
            print("self.all_tasks : ", self.all_tasks.count())
            self.all_tasks = self.all_tasks.filter(
                created_at__gte=self.date_from, importance__gte=importance, task_manager=task_manager
            )

        return self.all_tasks

    def get(self, request):
        # all_tasks_in_month = self.all_tasks.filter(
        #     created_at__gte=self.one_month_ago, importance__gte=3
        # )

        tasks_in_ready_list = self.get_all_tasks(request).filter(
            in_progress=False, is_testing=False, task_completed=False
        )
        tasks_in_progress_list = self.get_all_tasks(request).filter(
            in_progress=True, is_testing=False
        )
        tasks_in_testing_list = self.get_all_tasks(request).filter(
            in_progress=True, is_testing=True, task_completed=False
        )
        tasks_in_completed_list = self.get_all_tasks(request).filter(
            task_completed=True
        )

        all_tasks_in_month_serializer = ProjectProgressListSerializer(
            self.get_all_tasks(request), many=True)

        tasks_in_ready_serializer = ProjectProgressListSerializer(
            tasks_in_ready_list, many=True)
        tasks_in_progress_serializer = ProjectProgressListSerializer(
            tasks_in_progress_list, many=True)
        tasks_in_testing_serializer = ProjectProgressListSerializer(
            tasks_in_testing_list, many=True)
        tasks_in_completed_serializer = ProjectProgressListSerializer(
            tasks_in_completed_list, many=True)

        print("all_tasks (filter result): ", self.all_tasks.count())

        result_data = {
            "all_tasks_in_month": all_tasks_in_month_serializer.data,
            "tasks_in_ready": tasks_in_ready_serializer.data,
            "tasks_in_progress": tasks_in_progress_serializer.data,
            "tasks_in_testing": tasks_in_testing_serializer.data,
            "tasks_in_completed": tasks_in_completed_serializer.data,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateTaskInProgressView(APIView):

    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인 : pk ", pk)
        project_task = self.get_object(pk)

        if project_task.in_progress:
            message = "진행에서 준비중로 update"
            project_task.in_progress = False
            project_task.is_testing = False
            project_task.started_at_utc = None  # completed_at을 blank 상태로 만듦
            project_task.started_at_formatted = None  # completed_at을 blank 상태로 만듦

        else:
            message = "준비에서 작업중으로 update"
            project_task.in_progress = True
            project_task.started_at_utc = timezone.now()  # 현재 시간 저장

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateTaskIsTestingView(APIView):

    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인 : pk ", pk)
        project_task = self.get_object(pk)

        if project_task.is_testing:
            message = "테스트 진행 취소 update"
            project_task.is_testing = False

        else:
            message = "테스트 진행중으로 update"
            project_task.in_progress = True
            project_task.is_testing = True

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UncompletedTaskListViewForMe(APIView):
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

        if request.user.is_authenticated:
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, task_manager=request.user).order_by('-in_progress', '-created_at')
            count_for_all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, task_manager=request.user).count()
        else:
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False).order_by('-in_progress', '-created_at')
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

        # 직렬화
        serializer = ProjectProgressListSerializer(
            uncompleted_project_task_list_for_current_page, many=True)

        # 총 페이지 숫자 계산
        # if (count_for_all_completed_project_task_list % self.task_number_for_one_page == 0):
        #     self.totalCountForTask = count_for_all_completed_project_task_list
        # else:
        #     self.totalCountForTask = count_for_all_completed_project_task_list + 1

        self.totalCountForTask = math.trunc(
            count_for_all_uncompleted_project_task_list)

        count_for_ready = all_uncompleted_project_task_list.filter(
            in_progress=False).count()
        count_for_in_progress = all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=False, task_completed=False).count()
        count_for_in_testing = all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=True, task_completed=False).count()

        print("count_for_ready : ", count_for_ready)
        print("count_for_in_progress : ", count_for_in_progress)

        # step5 응답
        data = serializer.data
        data = {
            "count_for_ready": count_for_ready,
            "count_for_in_progress": count_for_in_progress,
            "count_for_in_testing": count_for_in_testing,

            "totalPageCount": self.totalCountForTask,
            "ProjectProgressList": data
        }
        return Response(data, status=HTTP_200_OK)


class UncompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []

    # all
    # within_a_week
    # within_a_month
    # over_a_month_ago

    def get(self, request):
        print("uncompleted task 요청 check !!")
        # step2 query 파라미터에서 page 가져오기 or 1
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        if period_option == "all":
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False).order_by('-in_progress', '-created_at')
        elif period_option == "within_a_week":
            one_week_ago = datetime.now() - timedelta(days=7)
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__gte=one_week_ago).order_by('-in_progress', '-created_at')
        elif period_option == "within_a_month":
            one_month_ago = datetime.now() - timedelta(days=30)
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__gte=one_month_ago).order_by('-in_progress', '-created_at')
        elif period_option == "over_a_month_ago":
            one_month_ago = datetime.now() - timedelta(days=30)
            all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__lt=one_month_ago).order_by('-in_progress', '-created_at')

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

        # 직렬화
        serializer = ProjectProgressListSerializer(
            uncompleted_project_task_list_for_current_page, many=True)

        # 총 페이지 숫자 계산
        # if (count_for_all_completed_project_task_list % self.task_number_for_one_page == 0):
        #     self.totalCountForTask = count_for_all_completed_project_task_list
        # else:
        #     self.totalCountForTask = count_for_all_completed_project_task_list + 1

        self.totalCountForTask = math.trunc(
            count_for_all_uncompleted_project_task_list)

        count_for_ready = all_uncompleted_project_task_list.filter(
            in_progress=False).count()
        count_for_in_progress = all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=False, task_completed=False).count()
        count_for_in_testing = all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=True, task_completed=False).count()

        # step5 응답
        data = serializer.data

        # 0412
        writers_info = get_writers_info(complete_status=False)

        response_data = {
            "writers_info": writers_info,
            "ProjectProgressList": data,
            "count_for_ready": count_for_ready,
            "count_for_in_progress": count_for_in_progress,
            "count_for_in_testing": count_for_in_testing,
            "totalPageCount": self.totalCountForTask,
            "task_number_for_one_page": self.task_number_for_one_page
        }
        return Response(response_data, status=HTTP_200_OK)


class CompletedTaskListViewForMe(APIView):
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

        if request.user.is_authenticated:
            all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, task_manager=request.user)
            count_for_all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, task_manager=request.user).count()
        else:
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

        self.totalCountForTask = math.trunc(
            count_for_all_completed_project_task_list)

        # step5 응답
        data = serializer.data

        writers_info = get_writers_info(complete_status=True)

        response__data = {
            "writers_info": writers_info,
            "totalPageCount": self.totalCountForTask,
            "ProjectProgressList": data
        }
        return Response(response__data, status=HTTP_200_OK)


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

        self.totalCountForTask = math.trunc(
            count_for_all_completed_project_task_list)

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
        print("project_task.extra_tasks ::::: ", project_task.extra_tasks)

        serializer = ProjectProgressDetailSerializer(
            project_task, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        print("put 요청 확인 ")
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


1122


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
        all_project_tasks = ProjectProgress.objects.all()[start:end]

        serializer = ProjectProgressListSerializer(
            all_project_tasks,
            many=True,
            context={"request": request}
        )

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

        print("request.data['task_manager] : ", request.data['task_manager'])

        serializer = CreateProjectProgressSerializer(data=request.data)
        if serializer.is_valid():
            # if request.user.is_authenticated:
            #     project_progress = serializer.save(task_manager=request.user)
            # else:
            #     project_progress = serializer.save()
            task_manager = User.objects.get(pk=request.data['task_manager'])

            project_progress = serializer.save(task_manager=task_manager)
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
            project_task.completed_at = None  # completed_at을 blank 상태로 만듦

        else:
            message = "비완료에서 완료로 update"
            project_task.task_completed = True
            new_completed_at = timezone.localtime()
            project_task.completed_at = new_completed_at  # 현재 시간 저장

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


class UpdateProjectStatusPageView(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("put 요청 확인")
        project_task = self.get_object(pk)

        status_to_move = request.data.get("status_to_move")
        if status_to_move == "ready":
            project_task.in_progress = False
            project_task.is_testing = False
            project_task.task_completed = False

        elif status_to_move == "in_progress":
            project_task.in_progress = True
            project_task.is_testing = False
            project_task.task_completed = False

        elif status_to_move == "is_testing":
            project_task.in_progress = True
            project_task.is_testing = True
            project_task.task_completed = False

        elif status_to_move == "complete":
            project_task.in_progress = False
            project_task.is_testing = False
            project_task.task_completed = True

        project_task.save()

        result_data = {
            "success": True,
            "message": f'update success <=> to {status_to_move} !!'
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateProjectTaskDueDate(APIView):

    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("put 요청 확인")

        # request body 에서 star_count 가져 오기
        due_date = request.data.get("due_date")

        # 해당 행 찾기
        project_task = self.get_object(pk)
        before_due_date = project_task.due_date

        # 업데이트할 값 설정 후 save()
        project_task.due_date = due_date
        result = project_task.save()
        print("update result for due date update : ", result)

        result_data = {
            "success": True,
            "message": f'start point update success from {before_due_date} to {due_date} '
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateProjectTaskStartedAt(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("put 요청 확인")
        # request body 에서 star_count 가져 오기
        started_at_for_update = request.data.get("started_at_for_update")

        # 해당 행 찾기
        project_task = self.get_object(pk)
        before_started_at = project_task.started_at

        # 업데이트할 값 설정 후 save()
        project_task.started_at_utc = started_at_for_update
        result = project_task.save()
        print("update result for due date update : ", result)

        result_data = {
            "success": True,
            "message": f'start point update success from {before_started_at} to {started_at_for_update} '
        }

        return Response(result_data, status=HTTP_200_OK)
