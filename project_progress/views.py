import calendar
import math
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from project_progress.serializers import CreateCommentSerializerForTask, CreateExtraTaskSerializer, CreateProjectProgressSerializer, CreateTestSerializerForOneTask, ProjectProgressDetailSerializer, ProjectProgressListSerializer, TestSerializerForOneTask, TestersForTestSerializer, UncompletedTaskSerializerForCashPrize
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ChallengersForCashPrize, ProjectProgress, ExtraTask, TaskComment, TestForTask, TestersForTest
from django.db.models import Count
from datetime import datetime, time
from django.utils import timezone

# taskListForChecked 1122
# class UpdateForTaskManagerForChecked(APIView):
#     def put(self, request, *args, **kwargs):
#         checked_row_pks = request.data.get('checkedRowPks', [])            # ex) checkedRowPks 는 [1,2,3,6] ProjectProgress 의 pk
#         selected_manager_pk = request.data.get('task_manager', None)        # ex) task_manager 는 ProjectProgress 의 task_manager의 pk


class UpdateForTaskManagerForChecked(APIView):
    def put(self, request, *args, **kwargs):
        # ex) checkedRowPks 는 [1,2,3,6] ProjectProgress 의 pk
        checked_row_pks = request.data.get('checkedRowPks', [])
        # ex) task_manager 는 ProjectProgress 의 task_manager
        selected_manager_pk = request.data.get('task_manager', None)

        if not checked_row_pks or not selected_manager_pk:
            return Response({"error": "Invalid data"}, status=HTTP_400_BAD_REQUEST)

        # 선택된 관리자를 가져옴
        selected_manager = User.objects.get(pk=selected_manager_pk)

        # checkedRowPks에 해당하는 ProjectProgress 객체들을 가져옴
        project_progress_list = ProjectProgress.objects.filter(
            pk__in=checked_row_pks)

        # 모든 가져온 ProjectProgress 객체의 task_manager를 selected_manager로 업데이트
        for project_progress in project_progress_list:
            project_progress.task_manager = selected_manager
            project_progress.save()

        return Response({"success": "Task manager updated"}, status=HTTP_200_OK)


class UpdateForTaskImportanceForChecked(APIView):
    def put(self, request, *args, **kwargs):
        # ex) checkedRowPks 는 [1,2,3,6] ProjectProgress 의 pk
        checked_row_pks = request.data.get('checkedRowPks', [])
        # ex) task_manager 는 ProjectProgress 의 task_manager
        importance = request.data.get('importance', None)

        print("importance:", importance)

        # checkedRowPks에 해당하는 ProjectProgress 객체들을 가져옴
        project_progress_list = ProjectProgress.objects.filter(
            pk__in=checked_row_pks)

        # 모든 가져온 ProjectProgress 객체의 task_manager를 selected_manager로 업데이트
        for project_progress in project_progress_list:
            project_progress.importance = importance
            project_progress.save()

        message = f"Task importance updated to {importance}."

        return Response({"message": message}, status=HTTP_200_OK)


class taskListForChecked(APIView):
    def get(self, request):
        checked_row_pks = request.query_params.getlist('checkedRowPks[]')
        print("체크된 pks for task list1 : ", checked_row_pks)
        print("체크된 pks for task list : ", checked_row_pks)
        # pk_list = checked_row_pks.split(',')
        # pk_list = [int(pk) for pk in pk_list]
        # all_project_tasks = ProjectProgress.objects.all()
        # pk_list = [int(pk) for pk in ','.join(checked_row_pks).split(',')]
        pk_list = [int(pk) for pk in checked_row_pks if pk]
        all_project_tasks = ProjectProgress.objects.filter(pk__in=pk_list)

        total_count = all_project_tasks.count()
        serializer = ProjectProgressListSerializer(
            all_project_tasks, many=True)

        serializer = ProjectProgressListSerializer(
            all_project_tasks,
            many=True,
            context={"request": request}
        )

        data = {
            "total_count": total_count,
            "ProjectProgressList": serializer.data
        }

        return Response(data, status=HTTP_200_OK)


# class UpdateViewForTaskDueDateForChecked(APIView):
#     def put(self, request):
#         # duration_option 값을 가져옵니다.
#         duration_option = request.data.get("duration_option")
#         # checkedRowPks 값을 가져옵니다.
#         checked_row_pks = request.data.get("checkedRowPks")

#         # pk가 checked_row_pks에 포함된 ProjectProgress 모델 인스턴스들의 due_date와 started_at_utc를 업데이트합니다.
#         updated_count = 0

#         if duration_option == "noon":
#             for pk in checked_row_pks:
#                 try:
#                     task = ProjectProgress.objects.get(pk=pk)
#                     task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
#                         timezone.now()).date(), time(hour=12)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
#                     # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
#                     task.started_at_utc = timezone.localtime(
#                         timezone.now()).astimezone(timezone.utc)
#                     task.save()
#                     updated_count += 1
#                 except ProjectProgress.DoesNotExist:
#                     pass

#         elif duration_option == "evening":
#             for pk in checked_row_pks:
#                 try:
#                     task = ProjectProgress.objects.get(pk=pk)
#                     task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
#                         timezone.now()).date(), time(hour=19)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
#                     # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
#                     task.started_at_utc = timezone.localtime(
#                         timezone.now()).astimezone(timezone.utc)
#                     task.save()
#                     updated_count += 1
#                 except ProjectProgress.DoesNotExist:
#                     pass

#         elif duration_option == "tomorrow":
#         elif duration_option == "day-after-tomorrow":
#         elif duration_option == "this-week":
#         elif duration_option == "this-month":


#         message = f"{updated_count} ProjectProgress instances updated." if updated_count > 0 else "No ProjectProgress instances updated."
#         return Response({'message': message}, status=HTTP_204_NO_CONTENT)
class UpdateViewForTaskDueDateForChecked(APIView):
    def put(self, request):
        # duration_option 값을 가져옵니다.
        duration_option = request.data.get("duration_option")
        # checkedRowPks 값을 가져옵니다.
        checked_row_pks = request.data.get("checkedRowPks")

        print("duration_option : ", duration_option)

        # pk가 checked_row_pks에 포함된 ProjectProgress 모델 인스턴스들의 due_date와 started_at_utc를 업데이트합니다.
        updated_count = 0

        if duration_option == "noon":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                        timezone.now()).date(), time(hour=12)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                    # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "evening":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                        timezone.now()).date(), time(hour=19)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                    # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "tomorrow":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(
                        timezone.localtime(timezone.now()).date() + timedelta(days=1), time(hour=19)))
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "day-after-tomorrow":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(
                        timezone.localtime(timezone.now()).date() + timedelta(days=2), time(hour=19)))
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "this-week":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    today = timezone.localtime(timezone.now()).date()
                    end_of_week = today + timedelta(days=(6 - today.weekday()))
                    task.due_date = timezone.make_aware(
                        datetime.combine(end_of_week, time(hour=19)))
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "this-month":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    today = timezone.localtime(timezone.now()).date()
                    # 이번 달의 마지막 날짜 구하기
                    last_day_of_month = today.replace(
                        day=calendar.monthrange(today.year, today.month)[1])
                    task.due_date = timezone.make_aware(
                        datetime.combine(last_day_of_month, time(hour=19)))
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        message = f"{updated_count} ProjectProgress instances updated." if updated_count > 0 else "No ProjectProgress instances updated."
        return Response({'message': message}, status=HTTP_204_NO_CONTENT)


class DeleteTasksForChecked(APIView):
    def delete(self, request):
        selected_buttons_data = request.data  # [1, 2, 3, 5]
        print("selected_buttons_data : ", selected_buttons_data)

        deleted_count = ProjectProgress.objects.filter(
            pk__in=selected_buttons_data).delete()[0]

        return Response({
            'message': f'{deleted_count} StudyNoteContent instances deleted.'
        })


class UpatedChallengersForCashPrize(APIView):

    def put(self, request, taskPk):
        message = ""
        print("put 요청 확인 : pk ", taskPk)

        if not request.user.is_authenticated:
            raise NotAuthenticated

        is_challenger_aready_exists = ChallengersForCashPrize.objects.filter(
            task=taskPk, challenger=request.user).exists()

        if is_challenger_aready_exists == False:
            task = ProjectProgress.objects.get(pk=taskPk)
            new_challenger_for_test = ChallengersForCashPrize(
                task=task, challenger=request.user)
            new_challenger_for_test.save()
            message = "챌린저 등록 성공"

        else:
            ChallengersForCashPrize.objects.filter(
                task=taskPk).delete()
            message = "챌린저 등록 취소 성공 !"

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class TasksWithCashPrize(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []
    user_for_search = ""

    # get 요청에 대해 처리
    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option 가져 오기
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        # 검색을 위한 user name 가져오기 (필수 아님)
        self.user_for_search = request.query_params.get(
            "username_for_search", "")
        print("self.user_for_search : ", self.user_for_search)

        # self.all_uncompleted_project_task_list 초기화 하기 for period option
        if period_option == "all":
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                is_task_for_cash_prize=True).order_by('-check_for_cash_prize', '-created_at')
        elif period_option == "within_a_week":
            one_week_ago = datetime.now() - timedelta(days=7)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                created_at__gte=one_week_ago, is_task_for_cash_prize=True).order_by('-check_for_cash_prize', '-created_at')
        elif period_option == "within_a_month":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                created_at__gte=one_month_ago, is_task_for_cash_prize=True).order_by('-check_for_cash_prize', '-created_at')
        elif period_option == "over_a_month_ago":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                created_at__lt=one_month_ago, is_task_for_cash_prize=True).order_by('-check_for_cash_prize', '-created_at')

        # total count 초기화
        if self.user_for_search == "":
            count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
                is_task_for_cash_prize=True).count()
        else:
            count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
                task_manager__username=self.user_for_search, is_task_for_cash_prize=True).count()

        print("count_for_all_uncompleted_project_task_list : ",
              count_for_all_uncompleted_project_task_list)

        self.totalCountForTask = math.trunc(
            count_for_all_uncompleted_project_task_list)

        # 페이지에 해당하는 list 정보 초기화
        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page

        if self.user_for_search != "":
            print("#####################################")
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                task_manager__username=self.user_for_search, is_task_for_cash_prize=True)
        else:
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
                start:end]

        # 직렬화
        serializer = UncompletedTaskSerializerForCashPrize(
            self.uncompleted_project_task_list_for_current_page, many=True)

        if self.user_for_search == "":
            count_for_ready = self.all_uncompleted_project_task_list.filter(
                in_progress=False, is_task_for_cash_prize=True).count()
            count_for_in_progress = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=False, task_completed=False, is_task_for_cash_prize=True).count()
            count_for_in_testing = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=True, task_completed=False, is_task_for_cash_prize=True).count()
        else:
            serializer = UncompletedTaskSerializerForCashPrize(
                self.uncompleted_project_task_list_for_current_page, many=True)
            # , task_manager = self.user_for_search
            count_for_ready = self.all_uncompleted_project_task_list.filter(
                in_progress=False, task_manager__username=self.user_for_search, is_task_for_cash_prize=True).count()
            count_for_in_progress = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=False, task_completed=False, task_manager__username=self.user_for_search, is_task_for_cash_prize=True).count()
            count_for_in_testing = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=True, task_completed=False, task_manager__username=self.user_for_search, is_task_for_cash_prize=True).count()

        print("count_for_ready,count_for_in_progress, count_for_in_testing : ",
              count_for_ready, count_for_in_progress, count_for_in_testing)

        # 리스트 직렬화
        data = serializer.data

        # 작성자 목록
        writers_info = get_writers_info_for_cash_prize(complete_status=False)

        print("writers_info : ", writers_info)

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


class SearchByUsername(APIView):
    def get(self, request):
        username = request.data.get('username')
        print("username : ", username)
        pass


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


def get_writers_info_for_cash_prize(complete_status):
    print("complete_status2 : ", complete_status)
    task_manager_counts = ProjectProgress.objects.filter(is_task_for_cash_prize=True).values(
        'task_manager__username', 'task_manager__profile_image', 'task_manager__cash').annotate(count=Count('id')).order_by('-task_manager__cash')
    print("task_manager_counts : ", task_manager_counts)

    task_managers_info = []
    for task_manager_count in task_manager_counts:
        writer_info = {
            "username": task_manager_count['task_manager__username'],
            "profile_image": task_manager_count['task_manager__profile_image'],
            "cash": task_manager_count['task_manager__cash'],
            "task_count": task_manager_count['count']
        }
        task_managers_info.append(writer_info)

    return task_managers_info


def get_writers_info(complete_status):
    print("complete_status2 : ", complete_status)
    task_manager_counts = ProjectProgress.objects.filter(task_completed=complete_status).values(
        'task_manager__username', 'task_manager__profile_image', 'task_manager__cash').annotate(count=Count('id'))
    print("task_manager_counts : ", task_manager_counts)

    task_managers_info = []
    for task_manager_count in task_manager_counts:
        writer_info = {
            "username": task_manager_count['task_manager__username'],
            "profile_image": task_manager_count['task_manager__profile_image'],
            "cash": task_manager_count['task_manager__cash'],
            "task_count": task_manager_count['count']
        }
        task_managers_info.append(writer_info)

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

        task_manager = ""
        date_range = request.query_params.get('dateRange', 'thisMonth')

        task_manager = request.query_params.get(
            'taskManagerForFiltering', '')
        importance = request.query_params.get('importance', 1)
        # is_requested_for_help = request.query_params.get('isRequestedForHelp', False)
        # is_bounty_task = request.query_params.get('isBountyTask', False)

        # print("date_range, task_manager, importance : ",
        #       date_range, task_manager, importance)

        # if (task_manager != ""):
        #     task_manager = User.objects.get(pk=task_manager)

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
                created_at__gte=self.date_from,
                importance__gte=importance
            )
            print("self.all_tasks : ", self.all_tasks.count())

        else:
            self.all_tasks = self.all_tasks.filter(
                created_at__gte=self.date_from, importance__gte=importance,
                task_manager=task_manager
            )
            print("self.all_tasks : ", self.all_tasks.count())

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
            project_task.current_status = "ready"
            project_task.started_at_utc = None  # completed_at을 blank 상태로 만듦
            project_task.started_at_formatted = None  # completed_at을 blank 상태로 만듦

        else:
            message = "준비에서 작업중으로 update"
            project_task.in_progress = True
            project_task.current_status = "in_progress"
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
            project_task.current_status = "in_progress"

        else:
            message = "테스트 진행중으로 update"
            project_task.in_progress = True
            project_task.is_testing = True
            project_task.current_status = "testing"

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UncompletedTaskListViewForMe(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []

    # get 요청에 대해
    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option (기간에 대해 검색)
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        # task_status_for_search
        task_status_option = request.query_params.get(
            "task_status_for_search", "")
        print("task_status_option : ", task_status_option)
        due_date_option_for_filtering = request.query_params.get(
            "due_date_option_for_filtering", "")
        print("due_date_option_for_filtering : ",
              due_date_option_for_filtering)

        self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
            task_completed=False, task_manager=request.user).order_by('-in_progress', '-created_at')
        count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.count()
        print("총개수 for My Task : ", count_for_all_uncompleted_project_task_list)

        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page

        uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
            start:end]

        if task_status_option != "":
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                current_status=task_status_option)

        if due_date_option_for_filtering == "undecided":
            noon = time(hour=12, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), noon)
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date=None)

        if due_date_option_for_filtering == "until-noon":
            noon = time(hour=12, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), noon)
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-evening":
            print("due_date_option_for_filtering !!!!!!!!!!!! ")
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), evening)
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-tomorrow":
            print("due_date_option_for_filtering !!!!!!!!!!!! ")
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), evening)
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-the-day-after-tomorrow":
            print("due_date_option_for_filtering tomorrow !!!!!!!!!!!! ")
            tomorrow = datetime.today() + timedelta(days=2)
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(tomorrow, evening)
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-this-week":
            print("due_date_option_for_filtering this week !!!!!!!!!!!! ")
            today = datetime.today()
            # 이번 주의 마지막 날짜 계산
            last_day_of_week = today + timedelta(days=(6 - today.weekday()))
            # 이번 주 마지막 날짜의 오후 11시 59분 59초까지
            deadline = datetime.combine(
                last_day_of_week, time(hour=23, minute=59, second=59))
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-this-month":
            print("due_date_option_for_filtering this month !!!!!!!!!!!! ")
            today = datetime.today()
            # 이번 달의 마지막 날짜 계산
            last_day_of_month = datetime(
                today.year, today.month, 1) + timedelta(days=32)
            last_day_of_month = last_day_of_month.replace(
                day=1) - timedelta(days=1)
            # 이번 달 마지막 날짜의 오후 11시 59분 59초까지
            deadline = datetime.combine(
                last_day_of_month, time(hour=23, minute=59, second=59))
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        serializer = ProjectProgressListSerializer(
            uncompleted_project_task_list_for_current_page, many=True)

        self.totalCountForTask = math.trunc(
            count_for_all_uncompleted_project_task_list)

        count_for_ready = self.all_uncompleted_project_task_list.filter(
            in_progress=False).count()
        count_for_in_progress = self.all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=False, task_completed=False).count()
        count_for_in_testing = self.all_uncompleted_project_task_list.filter(
            in_progress=True, is_testing=True, task_completed=False).count()

        # step5 응답
        data = serializer.data
        data = {
            "ProjectProgressList": data,
            "task_number_for_one_page": self.task_number_for_one_page,
            "totalPageCount": self.totalCountForTask,
            "count_for_ready": count_for_ready,
            "task_number_for_one_page": self.task_number_for_one_page,
            "count_for_in_progress": count_for_in_progress,
            "count_for_in_testing": count_for_in_testing,
        }

        return Response(data, status=HTTP_200_OK)


class UncompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []
    completed_project_task_list_for_current_page = []
    user_for_search = ""

    # get 요청에 대해 처리
    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option 가져 오기
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")
        # task_status_for_search
        task_status_option = request.query_params.get(
            "task_status_for_search", "")
        print("task_status_option : ", task_status_option)

        # 검색을 위한 user name 가져오기 (필수 아님)
        self.user_for_search = request.query_params.get(
            "username_for_search", "")
        print("self.user_for_search : ", self.user_for_search)
        due_date_option_for_filtering = request.query_params.get(
            "due_date_option_for_filtering", "")
        print("due_date_option_for_filtering : ",
              due_date_option_for_filtering)

        # self.all_uncompleted_project_task_list 초기화 하기 for period option
        if period_option == "all":
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False).order_by('-is_testing', '-in_progress', '-created_at')
        elif period_option == "within_a_week":
            one_week_ago = datetime.now() - timedelta(days=7)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__gte=one_week_ago).order_by('-in_progress', '-created_at')
        elif period_option == "within_a_month":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__gte=one_month_ago).order_by('-in_progress', '-created_at')
        elif period_option == "over_a_month_ago":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                task_completed=False, created_at__lt=one_month_ago).order_by('-in_progress', '-created_at')

        # total count 초기화
        if self.user_for_search == "":
            count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
                task_completed=False).count()
        else:
            count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
                task_completed=False, task_manager__username=self.user_for_search).count()

        print("count_for_all_uncompleted_project_task_list : ",
              count_for_all_uncompleted_project_task_list)

        self.totalCountForTask = math.trunc(
            count_for_all_uncompleted_project_task_list)

        # 페이지에 해당하는 list 정보 초기화
        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page

        if self.user_for_search != "":
            print("#####################################")
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                task_manager__username=self.user_for_search)
        else:
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
                start:end]

        if task_status_option != "":
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                current_status=task_status_option)

        if due_date_option_for_filtering == "undecided":
            noon = time(hour=12, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), noon)
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date=None)

        if due_date_option_for_filtering == "until-noon":
            noon = time(hour=12, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), noon)
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-evening":
            print("due_date_option_for_filtering !!!!!!!!!!!! ")
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), evening)
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-tomorrow":
            print("due_date_option_for_filtering !!!!!!!!!!!! ")
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(datetime.today(), evening)
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-the-day-after-tomorrow":
            print("due_date_option_for_filtering tomorrow !!!!!!!!!!!! ")
            tomorrow = datetime.today() + timedelta(days=2)
            evening = time(hour=19, minute=10, second=0)
            deadline = datetime.combine(tomorrow, evening)
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-this-week":
            print("due_date_option_for_filtering this week !!!!!!!!!!!! ")
            today = datetime.today()
            # 이번 주의 마지막 날짜 계산
            last_day_of_week = today + timedelta(days=(6 - today.weekday()))
            # 이번 주 마지막 날짜의 오후 11시 59분 59초까지
            deadline = datetime.combine(
                last_day_of_week, time(hour=23, minute=59, second=59))
            self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        if due_date_option_for_filtering == "until-this-month":
            print("due_date_option_for_filtering this month !!!!!!!!!!!! ")
            today = datetime.today()
            # 이번 달의 마지막 날짜 계산
            last_day_of_month = datetime(
                today.year, today.month, 1) + timedelta(days=32)
            last_day_of_month = last_day_of_month.replace(
                day=1) - timedelta(days=1)
            # 이번 달 마지막 날짜의 오후 11시 59분 59초까지
            deadline = datetime.combine(
                last_day_of_month, time(hour=23, minute=59, second=59))
            uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                due_date__lte=deadline)

        # 직렬화
        serializer = ProjectProgressListSerializer(
            self.uncompleted_project_task_list_for_current_page, many=True)

        if self.user_for_search == "":
            count_for_ready = self.all_uncompleted_project_task_list.filter(
                in_progress=False).count()
            count_for_in_progress = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=False, task_completed=False).count()
            count_for_in_testing = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=True, task_completed=False).count()
        else:
            serializer = ProjectProgressListSerializer(
                self.uncompleted_project_task_list_for_current_page, many=True)
            # , task_manager = self.user_for_search
            count_for_ready = self.all_uncompleted_project_task_list.filter(
                in_progress=False, task_manager__username=self.user_for_search).count()
            count_for_in_progress = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=False, task_completed=False, task_manager__username=self.user_for_search).count()
            count_for_in_testing = self.all_uncompleted_project_task_list.filter(
                in_progress=True, is_testing=True, task_completed=False, task_manager__username=self.user_for_search).count()

        # 리스트 직렬화
        data = serializer.data

        # 작성자 목록
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


class CompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_completed_project_task_list = []
    completed_project_task_list_for_current_page = []
    user_for_search = ""

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

        # 검색을 위한 user name 가져오기 (필수 아님)
        self.user_for_search = request.query_params.get(
            "username_for_search", "")
        print("self.user_for_search : ", self.user_for_search)

        if period_option == "all":
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True).order_by('-in_progress', '-created_at')
        elif period_option == "within_a_week":
            one_week_ago = datetime.now() - timedelta(days=7)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__gte=one_week_ago).order_by('-in_progress', '-created_at')
        elif period_option == "within_a_month":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__gte=one_month_ago).order_by('-in_progress', '-created_at')
        elif period_option == "over_a_month_ago":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__lt=one_month_ago).order_by('-in_progress', '-created_at')

        # total count 초기화
        if self.user_for_search == "":
            count_for_all_completed_project_task_list = self.all_completed_project_task_list.filter(
                task_completed=True).count()

        else:
            count_for_all_completed_project_task_list = self.all_completed_project_task_list.filter(
                task_completed=True, task_manager__username=self.user_for_search).count()
            print("count_for_all_uncompleted_project_task_list : ",
                  count_for_all_completed_project_task_list)

        self.totalCountForTask = math.trunc(
            count_for_all_completed_project_task_list)

        # 페이지에 해당하는 list 정보 초기화
        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page

        if self.user_for_search != "":
            self.completed_project_task_list_for_current_page = self.all_completed_project_task_list.filter(
                task_manager__username=self.user_for_search)
        else:
            self.completed_project_task_list_for_current_page = self.all_completed_project_task_list[
                start:end]

        # 직렬화
        serializer = ProjectProgressListSerializer(
            self.completed_project_task_list_for_current_page, many=True)
        data = serializer.data

        # count_for_ready = self.all_completed_project_task_list.filter(
        #     in_progress=False).count()
        # count_for_in_progress = self.all_completed_project_task_list.filter(
        #     in_progress=True, is_testing=False, task_completed=False).count()
        # count_for_in_testing = self.all_completed_project_task_list.filter(
        #     in_progress=True, is_testing=True, task_completed=False).count()

        # 작성자 목록
        writers_info = get_writers_info(complete_status=True)
        print("writers_info : ", writers_info)

        # 응답할 데이터 설정
        # data = {
        #     "totalPageCount": self.totalCountForTask,
        #     "ProjectProgressList": data
        # }
        # return Response(data, status=HTTP_200_OK)

        response_data = {
            "ProjectProgressList": data,
            "totalPageCount": self.totalCountForTask,
            "writers_info": writers_info,
            # "count_for_ready": count_for_ready,
            # "count_for_in_progress": count_for_in_progress,
            # "count_for_in_testing": count_for_in_testing,
            "task_number_for_one_page": self.task_number_for_one_page
        }
        return Response(response_data, status=HTTP_200_OK)


class CompletedTaskListViewForMe(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_completed_project_task_list = []

    def get(self, request):
        print("uncompleted task 요청 check !!")

        # step2 query 파라미터에서 page 가져오기 or 1
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option (기간에 대해 검색)
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        self.all_completed_project_task_list = ProjectProgress.objects.filter(
            task_completed=True, task_manager=request.user)
        count_for_all_completed_project_task_list = self.all_completed_project_task_list.filter(
            task_completed=True, task_manager=request.user).count()

        # 완료 총개수
        print("count_for_all_completed_project_task_list : ",
              count_for_all_completed_project_task_list)

        start = (page - 1) * self.task_number_for_one_page
        end = start + self.task_number_for_one_page
        completed_project_task_list_for_current_page = self.all_completed_project_task_list[
            start:end]

        serializer = ProjectProgressListSerializer(
            completed_project_task_list_for_current_page, many=True)

        self.totalCountForTask = math.trunc(
            count_for_all_completed_project_task_list)

        # step5 응답
        data = serializer.data

        writers_info = get_writers_info(complete_status=True)

        response__data = {
            "writers_info": writers_info,
            "task_number_for_one_page": self.task_number_for_one_page,
            "totalPageCount": self.totalCountForTask,
            "ProjectProgressList": data
        }
        return Response(response__data, status=HTTP_200_OK)


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


# 1122
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
            project_task.current_status = "testing"
            project_task.completed_at = None  # completed_at을 blank 상태로 만듦

        else:
            message = "비완료에서 완료로 update"
            project_task.task_completed = True
            project_task.current_status = "completed"
            new_completed_at = timezone.localtime()
            project_task.completed_at = new_completed_at  # 현재 시간 저장

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class update_task_for_is_task_for_cash_prize(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인")
        project_task = self.get_object(pk)

        if project_task.is_task_for_cash_prize:
            message = "상금 대상에서 비상금 대상으로 update"
            project_task.is_task_for_cash_prize = False
            project_task.cash_prize = 0

        else:
            message = "상금 대상으로 update"
            project_task.is_task_for_cash_prize = True

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateScoreByTesterView(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인")
        project_task = self.get_object(pk)
        score_by_tester = request.data.get('score_by_tester')

        project_task.score_by_tester = score_by_tester
        message = f"{score_by_tester} 점으로 task score update"

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


# class Update(APIView):
#     def get_object(self, pk):
#         try:
#             return ProjectProgress.objects.get(pk=pk)
#         except ProjectProgress.DoesNotExist:
#             raise NotFound

#     def put(self, request, pk):
#         message = ""
#         print("put 요청 확인")
#         project_task = self.get_object(pk)

#         if project_task.check_result_by_tester:
#             message = "완료에서 비완료로 update"
#             project_task.check_result_by_tester = False
#             # project_task.task_completed = False
#             # project_task.current_status = "testing"
#             # project_task.completed_at = None  # completed_at을 blank 상태로 만듦

#         else:
#             message = "비완료에서 완료로 update"
#             project_task.check_result_by_tester = True
#             # project_task.task_completed = True
#             # project_task.current_status = "completed"
#             # new_completed_at = timezone.localtime()
#             # project_task.completed_at = new_completed_at  # 현재 시간 저장

#         project_task.save()

#         result_data = {
#             "success": True,
#             "message": message,
#         }

#         return Response(result_data, status=HTTP_200_OK)


class UpdateCheckForCashPrize(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인")
        project_task = self.get_object(pk)

        task_manager_pk = request.data.get("taskMangerPk")
        cash_prize = request.data.get("cash_prize")
        user = User.objects.get(pk=task_manager_pk)

        if project_task.check_for_cash_prize:
            message = "완료에서 비완료로 cash task check update"
            project_task.check_for_cash_prize = False
            user.cash -= cash_prize
            user.save()

            # project_task.task_completed = False
            # project_task.current_status = "testing"
            # project_task.completed_at = None  # completed_at을 blank 상태로 만듦

        else:
            message = "비완료에서 완료로 cash task check update"
            project_task.check_for_cash_prize = True
            user.cash += cash_prize
            user.save()
            # project_task.task_completed = True
            # project_task.current_status = "completed"
            # new_completed_at = timezone.localtime()
            # project_task.completed_at = new_completed_at  # 현재 시간 저장

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateCheckResultByTesterView(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인")
        project_task = self.get_object(pk)

        if project_task.check_result_by_tester:
            message = "완료에서 비완료로 update"
            project_task.check_result_by_tester = False
            # project_task.task_completed = False
            # project_task.current_status = "testing"
            # project_task.completed_at = None  # completed_at을 blank 상태로 만듦

        else:
            message = "비완료에서 완료로 update"
            project_task.check_result_by_tester = True
            # project_task.task_completed = True
            # project_task.current_status = "completed"
            # new_completed_at = timezone.localtime()
            # project_task.completed_at = new_completed_at  # 현재 시간 저장

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateForCashPrizeForTask(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("put 요청 확인")

        # request body 에서 star_count 가져 오기
        cash_prize_for_update = request.data.get("cash_prize_for_update")

        # 해당 행 찾기
        project_task = self.get_object(pk)
        before_cash_prize = project_task.cash_prize

        # 업데이트할 값 설정 후 save()
        project_task.cash_prize = cash_prize_for_update
        project_task.save()

        result_data = {
            "success": True,
            "message": f'start point update success from {before_cash_prize} to {project_task.cash_prize} '
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
