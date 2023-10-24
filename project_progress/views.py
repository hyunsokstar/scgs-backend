import calendar
from django.db import transaction
import math
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta, time, date

# from project_progress.serializers import CreateCommentSerializerForExtraTask, CreateCommentSerializerForTask, CreateExtraTaskSerializer, CreateProjectProgressSerializer, CreateTestSerializerForOneTask, ExtraTasksDetailSerializer, ExtraTasksSerializer, ProjectProgressDetailSerializer, ProjectProgressListSerializer, TaskSerializerForToday, TaskUrlForExtraTaskSerializer, TaskUrlForTaskSerializer, TestSerializerForOneTask, TestersForTestSerializer, UncompletedTaskSerializerForCashPrize, TaskLogSerializer
from project_progress.serializers import (
    CreateCommentSerializerForExtraTask,
    CreateCommentSerializerForTask,
    CreateExtraTaskSerializer,
    CreateProjectProgressSerializer,
    CreateTestSerializerForOneTask,
    ExtraTasksDetailSerializer,
    ExtraTasksSerializer,
    ProjectProgressDetailSerializer,
    ProjectProgressListSerializer,
    SerializerForTaskListForSelectTargetForIntergration,
    SerializerForUncompletedTaskDetailListForChecked,
    TaskSerializerForToday,
    TaskUrlForExtraTaskSerializer,
    TaskUrlForTaskSerializer,
    TestSerializerForOneTask,
    UncompletedTaskSerializerForCashPrize,
    TaskLogSerializer,
    CreateTestSerializerForExtraTask,
    CompletedTaskSerializer,
    TargetTaskSerializer,
    SerializerForAllExtraTaskList
)
from django.db.models.functions import TruncDate
import pandas as pd
import pytz
from django.db.models import Q, F, Max, Count
from django.http import JsonResponse
from collections import defaultdict
from django.db.models.functions import ExtractWeekDay
from .models import (
    ChallengersForCashPrize,
    ProjectProgress,
    ExtraTask,
    TaskComment,
    TestForTask,
    TestersForTest,
    TaskLog,
    TaskUrlForTask,
    TaskUrlForExtraTask,
    ExtraTaskComment,
    TestForExtraTask,
    TestersForTestForExtraTask,
    ExtraManager
)
from django.shortcuts import get_object_or_404

# 1122
# CreateViewForExtraTaskManager


class CreateViewForExtraTaskManager(APIView):
    def post(self, request, targetTaskId):
        try:
            # targetTaskId에 해당하는 ProjectProgress 객체 가져오기
            target_task = ProjectProgress.objects.get(pk=targetTaskId)
            userNameForRegister = request.data.get('userNameForRegister')
            task_manager_to_register = User.objects.get(
                username=userNameForRegister)

            # ExtraManager 생성
            extra_manager = ExtraManager.objects.create(
                original_task=target_task,
                task_manager=task_manager_to_register,  # 현재 로그인한 사용자를 task_manager로 설정
            )

            # 성공 메시지 응답
            return Response(
                {"message": "ExtraManager가 성공적으로 생성되었습니다."},
                status=HTTP_201_CREATED,
            )
        except ProjectProgress.DoesNotExist:
            return Response(
                {"message": "targetTaskId에 해당하는 ProjectProgress를 찾을 수 없습니다."},
                status=HTTP_404_NOT_FOUND,
            )


class DeleteViewForExtraManagerForTask(APIView):
    def delete(self, request, extraManagerId):
        try:
            extra_manager = ExtraManager.objects.get(pk=extraManagerId)

            extra_manager.delete()
            return Response(
                {"message": "${extra_manager.task_manager.username} 님을 삭제 하였습니다 !"},
                status=HTTP_200_OK)

            # 현재 로그인한 사용자와 extra_manager.task_manager를 비교하여 권한 확인
            # if extra_manager.task_manager == request.user:
            #     extra_manager.delete()
            #     return Response(
            #         {"message": "${extra_manager.task_manager.username} 님을 삭제 하였습니다 !"},
            #         status=HTTP_200_OK)
            # else:
            #     return Response(
            #         {"message": f"{extra_manager.task_manager.username} 님만 삭제할 수 있습니다."},
            #         status=HTTP_403_FORBIDDEN  # 권한이 없는 경우 403 Forbidden 응답
            #     )

        except ExtraManager.DoesNotExist:
            print("extra_manager를 찾지 못했습니다")
            return Response(status=HTTP_404_NOT_FOUND)


class PostViewForRevertTaskForExtraTaskForCheckedFromSelectedOne(APIView):
    @transaction.atomic
    def post(self, request):
        checkedRowsForConvertForRevert = request.data.get(
            'checkedRowsForConvertForRevert', [])
        print("checkedRowsForConvertForRevert 1111111111111 ",
              checkedRowsForConvertForRevert)

        try:
            # checkedRowPks에 해당하는 ProjectProgress 객체들을 가져와서 처리합니다.
            for selected_pk in checkedRowsForConvertForRevert:
                selected_task = ExtraTask.objects.get(
                    pk=selected_pk)

                new_task = ProjectProgress()

                # ExtraTask로 필드 값을 복사합니다.
                new_task.task_manager = selected_task.task_manager
                new_task.task = selected_task.task
                new_task.task_description = selected_task.task_description
                new_task.due_date = selected_task.due_date
                new_task.save()

                # ProjectProgress를 삭제합니다.
                selected_task.delete()

            return Response({'message': '체크한 업무들을 revert 하였습니다'})
        except Exception as e:
            # 예외 메시지를 가져와서 반환합니다.
            error_message = str(e)
            return Response({'message': f'{error_message}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ListViewForgetTaskListWithoutOneForTaskIntergration(APIView):
    listForTask = []
    perPage = 15
    totalCountForTaskList = 0

    def get(self, request, selectedTaskPk):
        pageNum = request.query_params.get("pageNum", 1)
        pageNum = int(pageNum)
        checkedRowPks = request.query_params.getlist("checkedRowPks[]")
        checkedRowPks = [int(pk) for pk in checkedRowPks]

        print("params: ", request.query_params)
        # list_for_task = ProjectProgress.objects.all().order_by('-created_at')
        # list_for_task 구할때 ProjectProgress중에서 id 가 selectedTaskPk 인거 제외 하려면?
        list_for_task = ProjectProgress.objects.exclude(
            id=selectedTaskPk).order_by('-created_at')
        print("list_for_task : ", list_for_task)

        # step1 클래스 변수에 리스트 정보 담기
        self.listForTask = list_for_task
        # step2 클래스 변수에 리스트 총 개수 담기
        self.totalCountForTaskList = self.listForTask.count()
        # step3 특정 페이지에 대한 리스트 정보 클래스 변수에 담기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.listForTask = self.listForTask[start:end]

        # step4 클래스 변수에 담긴 리스트 정보 직렬화 하기
        serializer = SerializerForTaskListForSelectTargetForIntergration(
            self.listForTask, many=True)

        task_managers = list_for_task.values('task_manager__username').annotate(
            task_manager_count=Count('task_manager__username')).distinct().order_by('task_manager__username')

        # step5 응답할 페이지 네이션 관련 리스트 정보 딕셔너리로 선언 하기
        response_data = {
            "listForTask": serializer.data,
            "totalCountForTaskList": self.totalCountForTaskList,
            "perPage": self.perPage,
            "taskManagers": task_managers
        }

        # step6 step5에서 선언한 페이지 네이션 데이터 응답하도록 수정
        # return Response(serializer.data, status=HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)


class TransformViewCheckedTasksToTargetTask(APIView):
    @transaction.atomic
    def post(self, request):
        checkedRowsForConvert = request.data.get('checkedRowsForConvert', [])
        selectedTaskPk = request.data.get('selectedTaskPk', None)
        print("checkedRowsForConvert ::::::::::::::::::::::::::: ",
              checkedRowsForConvert)

        try:
            # selectedTargetPk에 해당하는 ProjectProgress 객체를 가져옵니다.
            selected_project_progress = ProjectProgress.objects.get(
                pk=selectedTaskPk)
            # 새로운 ExtraTask 생성
            # target_task = ExtraTask()
            # checkedRowPks에 해당하는 ProjectProgress 객체들을 가져와서 처리합니다.
            for project_progress_pk in checkedRowsForConvert:
                project_progress = ProjectProgress.objects.get(
                    pk=project_progress_pk)

                target_task = ExtraTask()

                # ExtraTask로 필드 값을 복사합니다.
                target_task.original_task = selected_project_progress
                target_task.task_manager = selected_project_progress.task_manager
                target_task.task = project_progress.task
                target_task.task_description = project_progress.task_description
                target_task.due_date = project_progress.due_date
                target_task.save()

                # ProjectProgress를 삭제합니다.
                project_progress.delete()

            return Response({'message': '체크한 업무들을 선택한 업무의 기타 업무로 전환 하였습니다.'})
        except Exception as e:
            # 예외 메시지를 가져와서 반환합니다.
            error_message = str(e)
            return Response({'message': f'{error_message}'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class SearchViewForTargetTasksForIntergration(APIView):

    def perform_search(self, searchWords, checkedRowPks):
        print("perform : ", searchWords, checkedRowPks)

        # 검색어를 사용하여 ProjectProgress 모델의 task 필드를 부분적으로 검색
        list_for_task = ProjectProgress.objects.exclude(
            id__in=checkedRowPks
        ).filter(task__icontains=searchWords).order_by('-created_at')

        return list_for_task

    def get(self, request):
        searchWords = request.query_params.get("searchWords")
        checkedRowPks = request.query_params.getlist("checkedRowPks[]")
        checkedRowPks = [int(pk) for pk in checkedRowPks]
        print(
            f"searchWords : ${searchWords}, checkedRowPks : ${checkedRowPks}")

        search_results = self.perform_search(searchWords, checkedRowPks)
        num_results = search_results.count()

        # SerializerForTaskListForSelectTargetForIntergration
        serializer = SerializerForTaskListForSelectTargetForIntergration(
            search_results, many=True)

        # 메시지 생성
        message = f"search result {num_results} 개 by {searchWords}"

        # JSON 응답 데이터 생성
        response_data = {
            "message": message,
            "searchWords": searchWords,
            "results": serializer.data,
        }

        # Response 객체 생성
        return Response(response_data, status=HTTP_200_OK)

# ListViewForExtraTask


class ListViewForExtraTask(APIView):
    def get(self, request):
        try:
            extra_tasks = ExtraTask.objects.all()
            serializer = SerializerForAllExtraTaskList(extra_tasks, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class DetailViewForTargetTaskForTaskIntegration(APIView):
    def get_object(self, taskId):
        try:
            return ProjectProgress.objects.get(pk=taskId)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def get(self, request, taskId):
        print("견적 디테일 페이지 요청 확인 (백엔드) !")
        print(taskId, type(taskId))

        project_task = self.get_object(taskId)
        print("project_task : ", project_task)
        print("project_task.extra_tasks ::::: ", project_task.extra_tasks)

        serializer = TargetTaskSerializer(
            project_task, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        print("put 요청 확인 ")
        print("request.data", request.data)
        print("pk : ", pk)

        project_task = self.get_object(pk)
        print("project_task : ", project_task)

        serializer = TargetTaskSerializer(
            project_task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                project_task = serializer.save()
                serializer = TargetTaskSerializer(project_task)
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


class ListViewForGetTaskListForTaskIntegration(APIView):
    listForTask = []
    perPage = 20
    totalCountForTaskList = 0

    def get(self, request):
        pageNum = request.query_params.get("pageNum", 1)
        pageNum = int(pageNum)
        checkedRowPks = request.query_params.getlist("checkedRowPks[]")
        checkedRowPks = [int(pk) for pk in checkedRowPks]

        print("params: ", request.query_params)

        # list_for_task = ProjectProgress.objects.all().order_by('-created_at')
        list_for_task = ProjectProgress.objects.exclude(
            id__in=checkedRowPks).order_by('-created_at')
        print("list_for_task : ", list_for_task)

        # step1 클래스 변수에 리스트 정보 담기
        self.listForTask = list_for_task
        # step2 클래스 변수에 리스트 총 개수 담기
        self.totalCountForTaskList = self.listForTask.count()
        # step3 특정 페이지에 대한 리스트 정보 클래스 변수에 담기
        start = (pageNum - 1) * self.perPage
        end = start + self.perPage
        self.listForTask = self.listForTask[start:end]

        # step4 클래스 변수에 담긴 리스트 정보 직렬화 하기
        serializer = SerializerForTaskListForSelectTargetForIntergration(
            self.listForTask, many=True)

        task_managers = list_for_task.values('task_manager__username').annotate(
            task_manager_count=Count('task_manager__username')).distinct().order_by('task_manager__username')

        # step5 응답할 페이지 네이션 관련 리스트 정보 딕셔너리로 선언 하기
        response_data = {
            "listForTask": serializer.data,
            "totalCountForTaskList": self.totalCountForTaskList,
            "perPage": self.perPage,
            "taskManagers": task_managers
        }

        # step6 step5에서 선언한 페이지 네이션 데이터 응답하도록 수정
        # return Response(serializer.data, status=HTTP_200_OK)
        return Response(response_data, status=HTTP_200_OK)


class DeleteCompletedTasksForChecked(APIView):
    def delete(self, request):
        selected_buttons_data = request.data  # [1, 2, 3, 5]
        print("selected_buttons_data : ", selected_buttons_data)

        deleted_count = ProjectProgress.objects.filter(
            pk__in=selected_buttons_data).delete()[0]

        return Response({
            'message': f'{deleted_count} StudyNoteContent instances deleted.'
        })

# class UpdateViewForTaskDueDateForDueDateOption(APIView):
#     def put(self, request, pk):
#         due_date_option = request.data.get("due_date_option")
#         # due_date_option  이
#         # until-noon 일 경우 pk에 해당하는 ProjectProgress.due_date 를 12시 59분
#         # until-evening 일 경우 pk에 해당하는  ProjectProgress.due_date 를 18시 59분
#         # until-morning 일 경우 pk에 해당하는  ProjectProgress.due_date 를 23시 59분


class UpdateViewForTaskDueDateForOneTask(APIView):
    def put(self, request):
        # duration_option 값을 가져옵니다.
        duration_option = request.data.get("duration_option")
        # checkedRowPks 값을 가져옵니다.
        pk = request.data.get("taskPk")

        print("UpdateViewForTaskDueDateForOneTask check !!!!!!!!!!!!!!!!!!!!!!!!!")
        print("duration_option : ", duration_option)

        # pk가 checked_row_pks에 포함된 ProjectProgress 모델 인스턴스들의 due_date와 started_at_utc를 업데이트합니다.
        updated_count = 0

        if duration_option == "until-noon":
            try:
                task = ProjectProgress.objects.get(pk=pk)
                task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=12, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                task.started_at_utc = timezone.localtime(
                    timezone.now()).astimezone(timezone.utc)
                task.save()
                updated_count += 1
            except ProjectProgress.DoesNotExist:
                pass

        elif duration_option == "until-evening":
            try:
                task = ProjectProgress.objects.get(pk=pk)
                task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=18, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
                task.started_at_utc = timezone.localtime(
                    timezone.now()).astimezone(timezone.utc)
                task.save()
                updated_count += 1
            except ProjectProgress.DoesNotExist:
                pass

        elif duration_option == "until-night":
            try:
                task = ProjectProgress.objects.get(pk=pk)
                task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=23, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
                task.started_at_utc = timezone.localtime(
                    timezone.now()).astimezone(timezone.utc)
                task.save()
                updated_count += 1
            except ProjectProgress.DoesNotExist:
                pass

        message = f"task due_date is updated !!"
        return Response({'message': message}, status=HTTP_204_NO_CONTENT)


class UpdateViewForTaskDueDateForDueDateOption(APIView):
    def put(self, request, pk):
        due_date_option = request.data.get("due_date_option")
        project_progress = get_object_or_404(ProjectProgress, pk=pk)

        if due_date_option == "until-morning":
            # Set the due date to 12:59 PM
            project_progress.due_date = project_progress.due_date.replace(
                hour=12, minute=59)
        elif due_date_option == "until-evening":
            # Set the due date to 6:59 PM
            project_progress.due_date = project_progress.due_date.replace(
                hour=18, minute=59)
        elif due_date_option == "until-night":
            # Set the due date to 11:59 PM
            project_progress.due_date = project_progress.due_date.replace(
                hour=23, minute=59)

        project_progress.save()

        return Response({"message": "Due date updated successfully."}, status=200)


class DeleteViewForTestForExtraTask(APIView):
    def get_object(self, taskPk):
        try:
            return TestForExtraTask.objects.get(pk=taskPk)
        except TestForExtraTask.DoesNotExist:
            raise NotFound

    def delete(self, request, testPk):
        print("삭제 요청 확인")
        test_for_task = self.get_object(testPk)
        test_for_task.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class UpateViewForTesterForExtraTask(APIView):

    def put(self, request, testPk):
        message = ""
        print("put 요청 확인 : pk ", testPk)

        if not request.user.is_authenticated:
            raise NotAuthenticated

        is_tester_aready_exists = TestersForTestForExtraTask.objects.filter(
            test=testPk, tester=request.user).exists()

        if is_tester_aready_exists == False:
            try:
                test = get_object_or_404(TestForExtraTask, pk=testPk)
                new_tester_for_test = TestersForTestForExtraTask(
                    test=test, tester=request.user)
                new_tester_for_test.save()
                message = "test check success"
            except TestForExtraTask.DoesNotExist:
                return JsonResponse({"error": "Test does not exist"}, status=404)

        else:
            TestersForTestForExtraTask.objects.filter(
                test=testPk).delete()
            message = "test check cancle !"

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


class UpdateViewForTestPassedForExtraTask(APIView):
    def get_object(self, pk):
        try:
            return TestForExtraTask.objects.get(pk=pk)
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


class UpdateViewForExtraCommentText(APIView):
    def get_object(self, pk):
        try:
            return ExtraTaskComment.objects.get(pk=pk)
        except ExtraTaskComment.DoesNotExist:
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


class DeleteViewForCommentForExtraTask(APIView):
    def get_object(self, pk):
        try:
            return ExtraTaskComment.objects.get(pk=pk)
        except ExtraTaskComment.DoesNotExist:
            raise NotFound

    def delete(self, request, commentPk):
        comment_obj = self.get_object(commentPk)
        comment_obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class CreateViewForCommentForExtraTask(APIView):

    print("comment 추가 요청 확인 !!!!!!!!!!!")

    def get_object(self, taskPk):
        try:
            return ProjectProgress.objects.get(pk=taskPk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def post(self, request, taskPk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = CreateCommentSerializerForExtraTask(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                # original_task = self.get_object(taskPk)
                test_for_task = serializer.save(writer=request.user)
                serializer = CreateExtraTaskSerializer(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")
        else:
            raise ParseError("Invalid data provided.")


class UpdateEditModeForCommentForExtraTask(APIView):
    def get_object(self, pk):
        try:
            return ExtraTaskComment.objects.get(pk=pk)
        except ExtraTaskComment.DoesNotExist:
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

        comment.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)

# deleteViewForExtraManagerForTask


class deleteViewForTaskUrlForExtraTask(APIView):
    def delete(self, request, pk):
        try:
            task_url_for_task = TaskUrlForExtraTask.objects.get(pk=pk)
            task_url_for_task.delete()
            return Response(status=HTTP_200_OK)
        except TaskUrlForExtraTask.DoesNotExist:
            print("taskUrl을 찾지 못했습니다")
            return Response(status=HTTP_404_NOT_FOUND)


class deleteViewForTaskUrlForTask(APIView):
    def delete(self, request, pk):
        try:
            task_url_for_task = TaskUrlForTask.objects.get(pk=pk)
            task_url_for_task.delete()
            return Response(status=HTTP_200_OK)
        except TaskUrlForTask.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class UpdateViewForTaskUrlForExtraTask(APIView):
    def put(self, request, pk):
        try:
            task_url_for_task = TaskUrlForExtraTask.objects.get(pk=pk)
            task_url_for_task.task_url = request.data.get('taskUrlForUpdate')
            task_url_for_task.save()
            return Response(status=HTTP_200_OK)
        except TaskUrlForExtraTask.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class UpdateViewForTaskUrlForTask(APIView):
    def put(self, request, pk):
        try:
            task_url_for_task = TaskUrlForTask.objects.get(pk=pk)
            task_url_for_task.task_url = request.data.get('taskUrlForUpdate')
            task_url_for_task.save()
            return Response(status=HTTP_200_OK)
        except TaskUrlForTask.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class CreateTaskUrlForTaskPk(APIView):
    def post(self, request, taskPk):
        # 1. task는 taskPk로 찾은 ProjectProgress
        try:
            print("taskPk : ", taskPk)
            task = ProjectProgress.objects.get(id=taskPk)
        except ProjectProgress.DoesNotExist:
            raise NotFound("Task not found")

        # 2. task_url = "http://"
        task_url = "http://example.com"

        # 3. serializer로 저장
        serializer = TaskUrlForTaskSerializer(data={
            "task": taskPk,
            "task_url": task_url,
        })

        # 4. serializer 무효할 시 parseerror 응답
        serializer.is_valid(raise_exception=True)

        # 5. 유효시 생성한 TaskUrlForTask 정보도 응답 http 200 응답
        task_url_for_task = serializer.save()
        serialized_data = TaskUrlForTaskSerializer(task_url_for_task).data
        return Response(serialized_data, status=HTTP_200_OK)


class CreateTaskUrlForExtraTask(APIView):
    def post(self, request, extraTaskPk):
        # 1. task는 taskPk로 찾은 ProjectProgress
        try:
            print("taskPk : ", extraTaskPk)
            task = ExtraTask.objects.get(id=extraTaskPk)
        except ExtraTask.DoesNotExist:
            raise NotFound("Task not found")

        # 2. task_url = "http://"
        task_url = "http://example.com"

        # 3. serializer로 저장
        serializer = TaskUrlForExtraTaskSerializer(data={
            "task": extraTaskPk,
            "task_url": task_url,
        })

        # 4. serializer 무효할 시 parseerror 응답
        serializer.is_valid(raise_exception=True)

        # 5. 유효시 생성한 TaskUrlForTask 정보도 응답 http 200 응답
        task_url_for_task = serializer.save()
        serialized_data = TaskUrlForTaskSerializer(task_url_for_task).data
        return Response(serialized_data, status=HTTP_200_OK)


class TaskStaticsIView2(APIView):
    def get(self, request):
        task_managers = ProjectProgress.objects.values_list(
            'task_manager', flat=True).distinct()

        response_data = {
            "managers": [],
            "task_count_for_month": []
        }

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

            response_data["managers"].append(manager_data)

        return Response(response_data)

# 1023 fix
# http://127.0.0.1:8000/api/v1/project_progress/task-log


class TaskLogView(APIView):

    totalCountForTaskLog = 0  # total_count 계산
    task_log_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_task_log_list = []
    selected_date = ""

    def get_user_obj_for_filtering_task_log(self, filterOptionForUserNameForTaskLogList):
        try:
            user = User.objects.get(
                username=filterOptionForUserNameForTaskLogList)
        except User.DoesNotExist:
            filterOptionForUserNameForTaskLogList = ""

        return user

    def get(self, request):
        filterOptionForUserNameForTaskLogList = request.GET.get(
            'filterOptionForUserNameForTaskLogList', "")

        days_of_week = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }


        # 요청에서 selectedDay 가져오기
        selectedDay = request.GET.get('selectedDay', "")

        if selectedDay == "":
            today_weekday = datetime.now().strftime('%A')
            selectedDay = today_weekday

        # 오늘의 날짜 얻기
        today = datetime.now()

        # 오늘로부터 몇 일 뒤의 날짜를 계산
        days_to_add = days_of_week[selectedDay] - today.weekday()
        selectedDaytime = today + timedelta(days=days_to_add)

        print("selectedDay 1111111111111111111111111111111 222222222222222222", selectedDaytime)

        # 오늘의 시작 시간 설정 (00:00:00)
        today_start = selectedDaytime.replace(hour=0, minute=0)

        # 오늘의 마지막 시간 설정 (23:59:59)
        today_end = selectedDaytime.replace(hour=23, minute=59)

        # 유저에 대한 리스트일 경우
        if filterOptionForUserNameForTaskLogList != "":
            user = self.get_user_obj_for_filtering_task_log(
                filterOptionForUserNameForTaskLogList)

            now = datetime.now(pytz.timezone('Asia/Seoul'))

            print("now :::::::: ", now)

            # today_start = datetime.combine(
            #     now.date(), time(hour=0, minute=0, second=0))
            # today_end = datetime.combine(now.date(), datetime.max.time())

            print("today_start :::::::::::::::::::::::::::", today_start)
            print("today_end :::::::::::::::::::::::::::", today_start)

            task_start = datetime.combine(
                now.date(), time(hour=9, minute=0, second=0), tzinfo=pytz.timezone('Asia/Seoul'))

            task_end = datetime.combine(now.date(), time(
                hour=19, minute=0, second=0), tzinfo=pytz.timezone('Asia/Seoul'))

            time_difference = now - task_start

            # time_difference를 초 단위로 변환
            total_seconds = time_difference.total_seconds()

            if total_seconds >= 0:
                # 시간이 양수 또는 0인 경우, 경과 시간을 계산
                hours_elapsed = int(total_seconds // 3600)
                minutes_elapsed = int((total_seconds % 3600) // 60)
                print(f"경과 시간: {hours_elapsed} 시간 {minutes_elapsed} 분")
                elapsed_time_string = f"경과 시간 {hours_elapsed} 시간 {minutes_elapsed} 분"

            else:
                # 시간이 음수인 경우, 남은 시간을 계산
                hours_elapsed = int((-total_seconds) // 3600)
                minutes_elapsed = int(((-total_seconds) % 3600) // 60)
                print(f"남은 시간: {hours_elapsed} 시간 {minutes_elapsed} 분")
                elapsed_time_string = f"남은 시간 {hours_elapsed} 시간 {minutes_elapsed} 분"

            # hours_elapsed = int(time_difference.total_seconds() // 3600)
            # minutes_elapsed = int(
            #     (time_difference.total_seconds() % 3600) // 60)

            # elapsed_time_string = f"{hours_elapsed} 시간 {minutes_elapsed} 분"

            total_today_task_count = ProjectProgress.objects.filter(
                task_manager=user,
                due_date__range=(today_start, today_end)
            ).count()

            total_today_uncompleted_task_count = ProjectProgress.objects.filter(
                task_manager=user,
                due_date__range=(today_start, today_end),
                task_completed=True
            ).count()

            total_today_completed_task_count = ProjectProgress.objects.filter(
                task_manager=user,
                due_date__range=(today_start, today_end),
                task_completed=True
            ).count()

            if hours_elapsed > 0:
                average_number_per_hour = round(
                    total_today_completed_task_count / hours_elapsed, 1)
            else:
                average_number_per_hour = 0

            task_logs = TaskLog.objects.filter(
                writer=user,
                completed_at__range=(today_start, today_end))

            writers = defaultdict(int)  # 작성자별 데이터 개수를 저장할 defaultdict 초기화

            for task_log in task_logs:
                print("check !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("task_log.writer : ", task_log.writer)
                writer = task_log.writer
                writers[writer.username] += 1

            print("task_logs ::::::::::::::::::::: ", task_logs)

            writers_data = []  # 작성자별 데이터를 저장할 리스트 초기화

            for writer, count in writers.items():
                writer_data = {
                    # 작성자의 유저네임 사용 (예시: writer.username)
                    'writer': writer,
                    'count': count,  # 해당 작성자의 데이터 개수
                }
                writers_data.append(writer_data)

            serializer = TaskLogSerializer(task_logs, many=True)
            task_log_data = serializer.data

            # todo1: 오늘이 포함된 주의 요일별 task count 구하기
            weekday_mapping = {
                1: 'Sunday',
                2: 'Monday',
                3: 'Tuesday',
                4: 'Wednesday',
                5: 'Thursday',
                6: 'Friday',
                7: 'Saturday'
            }

            today = timezone.localtime(timezone.now()).date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + \
                timedelta(days=6, hours=23, minutes=59, seconds=59)

            task_count_for_weekdays = ProjectProgress.objects.filter(
                completed_at__range=(start_of_week, start_of_week +
                                     timedelta(days=7, hours=23, minutes=59, seconds=59)),
                task_completed=True
            ).annotate(
                weekday=ExtractWeekDay(
                    'completed_at', tzinfo=pytz.timezone('Asia/Seoul'))
            ).values('weekday').annotate(count=Count('id'))

            task_count_for_weekdays = {
                weekday_mapping[entry['weekday']]: entry['count']
                for entry in task_count_for_weekdays
            }

            all_weekdays = ['Monday', 'Tuesday', 'Wednesday',
                            'Thursday', 'Friday', 'Saturday', 'Sunday']

            task_count_for_weekdays = {
                weekday: task_count_for_weekdays.get(weekday, 0)
                for weekday in all_weekdays
            }

            # todo2: 오늘 날짜의 정보 (날짜와 요일) 구하기
            today_info = {
                'date': now.strftime("%Y년 %m월 %d일"),
                'dayOfWeek': now.strftime('%A')
            }

        # 유저와 상관 없이 전체 리스트
        else:
            # Replace 'YOUR_TIMEZONE' with your desired timezone
            your_timezone = pytz.timezone('Asia/Seoul')
            now = datetime.now(your_timezone)

            # today_start = datetime.combine(now.date(), time(
            #     hour=0, minute=0, second=0), tzinfo=your_timezone)
            # today_end = datetime.combine(now.date(), datetime.max.time())

            task_start = datetime.now(your_timezone).replace(
                hour=9, minute=0, second=0, microsecond=0)


            time_difference = now - task_start

            print("now : ", now)
            print("task_start : ", task_start)
            print("time_difference : ", time_difference)

            # now = datetime.now()

            # # 목표 시간 설정 (오전 9시)
            # target_time = time(9, 0)

            # # 현재 날짜와 목표 시간을 결합하여 목표 시간의 datetime 객체 생성
            # target_datetime = datetime.combine(now.date(), target_time)

            # # 시간 차이 계산
            # time_difference = target_datetime - now

            # # 시간 차이 출력
            # print("현재 시간:", now)
            # print("목표 시간 (오전 9시):", target_datetime)
            # print("시간 차이:", time_difference)

            total_seconds = abs(
                time_difference.total_seconds())  # 양수로 변환하여 차이 계산

            hours_elapsed = int(total_seconds // 3600)
            minutes_elapsed = int((total_seconds % 3600) // 60)

            if now > task_start:
                elapsed_time_string = f"{hours_elapsed} 시간 {minutes_elapsed} 분 경과"
            else:
                hours_remaining = int(total_seconds // 3600)
                minutes_remaining = int((total_seconds % 3600) // 60)
                elapsed_time_string = f"시작하기까지 {hours_remaining} 시간 {minutes_remaining} 분"

            print("elapsed_time_string: ", elapsed_time_string)

            total_today_task_count = ProjectProgress.objects.filter(
                due_date__range=(today_start, today_end)
            ).count()

            print("total_today_task_count !!!!!!!!!!! ", total_today_task_count)

            total_today_completed_task_count = ProjectProgress.objects.filter(
                completed_at__range=(today_start, today_end),
                task_completed=True
            ).count()

            total_today_uncompleted_task_count = ProjectProgress.objects.filter(
                due_date__range=(today_start, today_end),
                task_completed=False
            ).count()

            if minutes_elapsed > 0:
                average_number_per_hour = total_today_completed_task_count / 10
                print("total_today_completed_task_count :;:::::::::::::::::::::::::::: ", total_today_completed_task_count)
                print("average_number_per_hour :::::::::::::::::::::::::::::::::::::::::::::: ", average_number_per_hour)
            else:
                average_number_per_hour = 0

            task_logs = TaskLog.objects.filter(
                completed_at__range=(today_start, today_end))

            print("task_logs :;:::::::::::::::: ", task_logs)

            writers = defaultdict(int)  # 작성자별 데이터 개수를 저장할 defaultdict 초기화

            for task_log in task_logs:
                print("check !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("task_log.writer : ", task_log.writer)
                writer = task_log.writer
                writers[writer.username] += 1

            print("writers ::::::::::::::::::::: ", writers)

            writers_data = []  # 작성자별 데이터를 저장할 리스트 초기화

            for writer, count in writers.items():
                writer_data = {
                    # 작성자의 유저네임 사용 (예시: writer.username)
                    'writer': writer,
                    'count': count,  # 해당 작성자의 데이터 개수
                }
                writers_data.append(writer_data)

            serializer = TaskLogSerializer(task_logs, many=True)
            task_log_data = serializer.data

            # todo1: 오늘이 포함된 주의 요일별 task count 구하기
            weekday_mapping = {
                1: 'Sunday',
                2: 'Monday',
                3: 'Tuesday',
                4: 'Wednesday',
                5: 'Thursday',
                6: 'Friday',
                7: 'Saturday'
            }

            today = timezone.localtime(timezone.now()).date()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + \
                timedelta(days=6, hours=23, minutes=59, seconds=59)

            task_count_for_weekdays = ProjectProgress.objects.filter(
                completed_at__range=(start_of_week, start_of_week +
                                     timedelta(days=7, hours=23, minutes=59, seconds=59)),
                task_completed=True
            ).annotate(
                weekday=ExtractWeekDay(
                    'completed_at', tzinfo=pytz.timezone('Asia/Seoul'))
            ).values('weekday').annotate(count=Count('id'))

            task_count_for_weekdays = {
                weekday_mapping[entry['weekday']]: entry['count']
                for entry in task_count_for_weekdays
            }

            all_weekdays = ['Monday', 'Tuesday', 'Wednesday',
                            'Thursday', 'Friday', 'Saturday', 'Sunday']

            task_count_for_weekdays = {
                weekday: task_count_for_weekdays.get(weekday, 0)
                for weekday in all_weekdays
            }

            # todo2: 오늘 날짜의 정보 (날짜와 요일) 구하기
            today_info = {
                'date': now.strftime("%Y년 %m월 %d일"),
                'dayOfWeek': now.strftime('%A')
            }

            # todo !!: 오늘이 포함된 주의 월화수목금토일 날짜 어떻게 구해?
            # 오늘의 날짜를 얻습니다.
            today = timezone.localtime(timezone.now()).date()

            # 오늘로부터 해당 주의 첫날을 계산합니다.
            start_of_week = today - timedelta(days=today.weekday())

            # 해당 주의 월화수목금토일을 구합니다.
            weekdays = [start_of_week + timedelta(days=i) for i in range(7)]

            # weekdays 리스트를 그대로 프론트로 보낼 때 UTC 형식으로 유지
            # weekdays_utc = [day.strftime('%Y-%m-%dT%H:%M:%SZ') for day in weekdays]

            # 이번주 월요일의 날짜 구하려면?

            
        # TaskStatusViewForToday
        response_data = {
            'total_today_task_count': total_today_task_count,
            'total_today_completed_task_count': total_today_completed_task_count,
            'total_today_uncompleted_task_count': total_today_uncompleted_task_count,
            'TaskLog': task_log_data,
            'average_number_per_hour': average_number_per_hour,
            'elapsed_time': elapsed_time_string,
            'writers': writers_data,
            'task_count_for_weekdays': task_count_for_weekdays,
            'today_info': today_info,
            # 'weekdays_utc': weekdays_utc
        }

        return Response(response_data, status=HTTP_200_OK)


# class TaskLogView(APIView):
#     totalCountForTaskLog = 0
#     task_log_number_for_one_page = 50
#     all_task_log_list = []

#     def get(self, request):
#         userOptionForList = request.GET.get('userOptionForList', "")

#         if userOptionForList != "":
#             response_data = self.get_user_task_log_data(userOptionForList)

#         else:
#             response_data = self.get_default_task_log_data()

#         return Response(response_data, status=HTTP_200_OK)


#     def get_user_task_log_data(self, username):
#         user = User.objects.get(username=username)
#         now = datetime.now(pytz.timezone('Asia/Seoul'))
#         today_start, task_start, today_end, task_end = self.get_time_range(now)

#         total_today_task_count = self.get_total_task_count_for_user(
#             user, today_start, today_end)
#         total_today_completed_task_count = self.get_completed_task_count_for_user(
#             user, today_start, today_end)
#         average_number_per_hour, elapsed_time_string = self.get_average_number_per_hour_for_user(
#             total_today_completed_task_count, task_start, task_end)
#         task_logs, writers_data = self.get_task_logs_and_writers_for_everyone(
#             user, today_start, today_end)
#         task_count_for_weekdays = self.get_task_count_for_weekdays(now)
#         today_info = self.get_today_info(now)


#         serializer = TaskLogSerializer(task_logs, many=True)
#         task_log_data = serializer.data

#         response_data = {
#             'total_today_task_count': total_today_task_count,
#             'total_today_completed_task_count': total_today_completed_task_count,
#             'TaskLog': task_log_data,
#             'average_number_per_hour': average_number_per_hour,
#             'elapsed_time': elapsed_time_string,
#             'writers': writers_data,
#             'task_count_for_weekdays': task_count_for_weekdays,
#             'today_info': today_info
#         }

#         return response_data

#     def get_default_task_log_data(self):
#         now = datetime.now(pytz.timezone('Asia/Seoul'))
#         today_start, task_start, today_end, task_end = self.get_time_range(now)
#         total_today_task_count = self.get_total_task_count_for_everyone(
#             today_start, today_end)
#         total_today_completed_task_count = self.get_completed_task_count_for_everyone(
#             today_start, today_end)
#         total_today_uncompleted_task_count = self.get_uncompleted_task_count(
#             today_start, today_end)
#         average_number_per_hour, elapsed_time_string = self.get_average_number_per_hour_for_everyone(
#             total_today_completed_task_count, task_start, task_end)
#         task_logs, writers_data = self.get_task_logs_and_writers_for_everyone(
#             today_start, today_end)
#         task_count_for_weekdays = self.get_task_count_for_weekdays(now)
#         today_info = self.get_today_info(now)

#         serializer = TaskLogSerializer(task_logs, many=True)
#         task_log_data = serializer.data

#         response_data = {
#             'total_today_task_count': total_today_task_count,
#             'total_today_completed_task_count': total_today_completed_task_count,
#             'total_today_uncompleted_task_count': total_today_uncompleted_task_count,
#             'TaskLog': task_log_data,
#             'average_number_per_hour': average_number_per_hour,
#             'elapsed_time': elapsed_time_string,
#             'writers': writers_data,
#             'task_count_for_weekdays': task_count_for_weekdays,
#             'today_info': today_info
#         }

#         return response_data

#     def get_time_range(self, now):
#         today_start = datetime.combine(
#             now.date(), time(hour=0, minute=0, second=0))
#         task_start = datetime.combine(now.date(), time(
#             hour=9, minute=0, second=0), tzinfo=pytz.timezone('Asia/Seoul'))
#         today_end = datetime.combine(now.date(), datetime.max.time())

#         task_end = datetime.combine(now.date(), time(
#             hour=19, minute=0, second=0), tzinfo=pytz.timezone('Asia/Seoul'))

#         return today_start, task_start, today_end, task_end

#     def get_total_task_count_for_user(self, user, today_start, today_end):

#         return ProjectProgress.objects.filter(
#             task_manager=user,
#             due_date__range=(today_start, today_end)
#         ).count()

#     def get_total_task_count_for_everyone(self, today_start, today_end):

#         return ProjectProgress.objects.filter(
#             due_date__range=(today_start, today_end)
#         ).count()

#     def get_completed_task_count_for_user(self, user, today_start, today_end):
#         return ProjectProgress.objects.filter(
#             task_manager=user,
#             due_date__range=(today_start, today_end),
#             task_completed=True
#         ).count()

#     def get_completed_task_count_for_everyone(self, today_start, today_end):
#         return ProjectProgress.objects.filter(
#             due_date__range=(today_start, today_end),
#             task_completed=True
#         ).count()

#     def get_uncompleted_task_count(self, today_start, today_end):
#         return ProjectProgress.objects.filter(
#             due_date__range=(today_start, today_end),
#             task_completed=False
#         ).count()

#     def get_average_number_per_hour_for_user(self, total_today_completed_task_count, task_start, task_end):
#         time_difference = task_end - task_start
#         hours_elapsed = int(time_difference.total_seconds() // 3600)
#         minutes_elapsed = int((time_difference.total_seconds() % 3600) // 60)
#         if hours_elapsed > 0:
#             average_number_per_hour = round(
#                 total_today_completed_task_count / hours_elapsed, 1)
#         else:
#             average_number_per_hour = 0
#         elapsed_time_string = f"{hours_elapsed} 시간 {minutes_elapsed} 분"
#         return average_number_per_hour, elapsed_time_string

#     def get_average_number_per_hour_for_everyone(self, total_today_completed_task_count, task_start, task_end):
#         time_difference = task_end - task_start
#         hours_elapsed = int(time_difference.total_seconds() // 3600)
#         minutes_elapsed = int((time_difference.total_seconds() % 3600) // 60)
#         if hours_elapsed > 0:
#             average_number_per_hour = round(
#                 total_today_completed_task_count / hours_elapsed, 1)
#         else:
#             average_number_per_hour = 0
#         elapsed_time_string = f"{hours_elapsed} 시간 {minutes_elapsed} 분"
#         return average_number_per_hour, elapsed_time_string

#     def get_task_logs_and_writers_for_user(self, user, today_start, today_end):
#         task_logs = TaskLog.objects.filter(
#             writer=user,
#             completed_at__range=(today_start, today_end)
#         )
#         writers = defaultdict(int)
#         for task_log in task_logs:
#             writer = task_log.writer
#             writers[writer.username] += 1
#         writers_data = []
#         for writer, count in writers.items():
#             writer_data = {
#                 'writer': writer,
#                 'count': count,
#             }
#             writers_data.append(writer_data)
#         serializer = TaskLogSerializer(task_logs, many=True)
#         task_log_data = serializer.data
#         return task_log_data, writers_data

#     def get_task_logs_and_writers_for_everyone(self, today_start, today_end):
#         task_logs = TaskLog.objects.filter(
#             # writer=user,
#             completed_at__range=(today_start, today_end)
#         )
#         writers = defaultdict(int)
#         for task_log in task_logs:
#             writer = task_log.writer
#             writers[writer.username] += 1
#         writers_data = []
#         for writer, count in writers.items():
#             writer_data = {
#                 'writer': writer,
#                 'count': count,
#             }
#             writers_data.append(writer_data)
#         serializer = TaskLogSerializer(task_logs, many=True)
#         task_log_data = serializer.data
#         return task_log_data, writers_data

#     def get_task_count_for_weekdays(self, now):
#         weekday_mapping = {
#             1: 'Sunday',
#             2: 'Monday',
#             3: 'Tuesday',
#             4: 'Wednesday',
#             5: 'Thursday',
#             6: 'Friday',
#             7: 'Saturday'
#         }
#         today = timezone.localtime(timezone.now()).date()
#         start_of_week = today - timedelta(days=today.weekday())
#         end_of_week = start_of_week + \
#             timedelta(days=6, hours=23, minutes=59, seconds=59)
#         task_count_for_weekdays = ProjectProgress.objects.filter(
#             completed_at__range=(start_of_week, start_of_week +
#                                  timedelta(days=7, hours=23, minutes=59, seconds=59)),
#             task_completed=True
#         ).annotate(weekday=ExtractWeekDay('completed_at', tzinfo=pytz.timezone('Asia/Seoul'))).values('weekday').annotate(count=Count('id'))
#         task_count_for_weekdays = {
#             weekday_mapping[entry['weekday']]: entry['count']
#             for entry in task_count_for_weekdays
#         }
#         all_weekdays = ['Monday', 'Tuesday', 'Wednesday',
#                         'Thursday', 'Friday', 'Saturday', 'Sunday']
#         task_count_for_weekdays = {
#             weekday: task_count_for_weekdays.get(weekday, 0)
#             for weekday in all_weekdays
#         }
#         return task_count_for_weekdays

#     def get_today_info(self, now):
#         today_info = {
#             'date': now.strftime("%Y년 %m월 %d일"),
#             'dayOfWeek': now.strftime('%A')
#         }
#         return today_info


class UpdateTaskTimeOptionAndOrder(APIView):
    def put(self, request):
        taskPk = request.data.get('taskPk')
        time_option = request.data.get('time_option')
        orgin_task_id = request.data.get('orgin_task_id')
        ordering_option = request.data.get('ordering_option')

        print(f"""
        received data :
        taskPk={taskPk},
        time_option={time_option},
        orgin_task_id={orgin_task_id},
        ordering_option={ordering_option}
        """)

        if ordering_option == "switch_order_of_two_tasks":
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # Fetch taskPk object
            task_to_update = ProjectProgress.objects.get(pk=taskPk)

            # Determine due_date based on time_option
            if time_option == 'morning_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=12, minute=59)))
            elif time_option == 'afternoon_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=18, minute=59)))
            elif time_option == 'night_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=23, minute=59)))

            print("time_option 11111111 ::::::::::::::::::::: ", time_option)

            # Assign time_option to due_date_option
            task_to_update.due_date_option = time_option

            # Fetch orgin_task_id object
            origin_task = ProjectProgress.objects.get(pk=orgin_task_id)
            task_to_update.order = origin_task.order - 1

            task_to_update.save()

            print("origin_task.order 22222222  ::::::::::  ", origin_task.order)

            filtered_records = ProjectProgress.objects.filter(
                due_date_option=time_option).exclude(id=taskPk).filter(order__lt=origin_task.order).order_by("-order")

            print("filtered_records 3333 :::::::::: ", filtered_records)

            # # origin_task.order
            order_offset = 2
            for record in filtered_records:
                record.order = origin_task.order - order_offset
                record.save()
                order_offset += 1

            filtered_records = ProjectProgress.objects.filter(
                due_date_option=time_option)

            # for i, record in enumerate(filtered_records, start=1):
            #     record.order = i
            #     record.save()
            #     print("new order : ", record.order)

            # for i, record in enumerate(filtered_records, start=1):
            #     record.order = i
            #     record.save()
            #     print("new order : " ,record.order)

        elif ordering_option == "move_to_last":
            task_to_update = ProjectProgress.objects.get(pk=taskPk)
            task_to_update.due_date_option = time_option

            # Fetch orgin_task_id object
            origin_tasks = ProjectProgress.objects.filter(
                due_date_option=time_option)

            # Find the largest order in origin_tasks
            max_order = origin_tasks.aggregate(Max('order'))['order__max']

            if time_option == 'morning_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=12, minute=59)))
            elif time_option == 'afternoon_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=18, minute=59)))
            elif time_option == 'night_tasks':
                task_to_update.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                    timezone.now()).date(), time(hour=23, minute=59)))

            if max_order is not None:
                task_to_update.order = max_order + 1
                print("time_option : ", time_option)
                task_to_update.due_date_option = time_option
            else:
                task_to_update.order = 1
                print("time_option : ", time_option)
                task_to_update.due_date_option = time_option

            task_to_update.save()

            filtered_records = ProjectProgress.objects.filter(
                due_date_option=time_option)

        return Response(status=HTTP_200_OK)


class TaskStatusViewForToday(APIView):
    def get(self, request):
        seoul_tz = pytz.timezone('Asia/Seoul')
        now = datetime.now().astimezone(seoul_tz)

        morning_start = now.replace(hour=0, minute=0)
        morning_end = now.replace(hour=13, minute=0)

        afternoon_start = morning_end
        afternoon_end = now.replace(
            hour=19, minute=0, second=10)

        night_start = now.replace(hour=19, minute=0, second=0)
        night_end = now.replace(hour=23, minute=59, second=59)

        morning_tasks = ProjectProgress.objects.filter(
            Q(due_date__gte=morning_start) &
            Q(due_date__lt=morning_end)
        ).order_by("task_completed", "order")
        afternoon_tasks = ProjectProgress.objects.filter(
            Q(due_date__gte=afternoon_start) &
            Q(due_date__lt=afternoon_end)
        ).order_by("task_completed", "order")
        night_tasks = ProjectProgress.objects.filter(
            Q(due_date__gte=night_start) &
            Q(due_date__lt=night_end)
        )
        # ).order_by("task_completed", "order")

        # due_date 가 오늘 날짜 이전이고 current_status 가 비완료(completed가 아닌 것들)인 개수 구해서 response_data에 추가
        task_count_for_uncompleted_task_until_yesterday = ProjectProgress.objects.filter(
            (Q(due_date__lt=morning_start)) & ~Q(
                current_status='completed')
        ).count()

        # due_date 가 오늘 날짜에 포함 되는것들에 대해 current_status 를 기준으로 ProjectProgress count 구해서 아래 항목 구한뒤 response_data 에 추가 하도록 하기

        task_count_for_ready = ProjectProgress.objects.filter(
            Q(due_date__date=now.date()) & Q(current_status='ready')
        ).count()
        task_count_for_in_progress = ProjectProgress.objects.filter(
            Q(due_date__date=now.date()) & Q(current_status='in_progress')
        ).count()
        task_count_for_testing = ProjectProgress.objects.filter(
            Q(due_date__date=now.date()) & Q(current_status='testing')
        ).count()

        task_count_for_completed = ProjectProgress.objects.filter(
            Q(due_date__date=now.date()) & Q(current_status='completed')
        ).count()

        toal_task_count_for_today = task_count_for_ready + \
            task_count_for_in_progress + task_count_for_testing + task_count_for_completed
        if toal_task_count_for_today != 0:
            progress_rate = int(
                (task_count_for_completed / toal_task_count_for_today) * 100)
        else:
            progress_rate = 0

        weekday_mapping = {
            1: 'Sunday',
            2: 'Monday',
            3: 'Tuesday',
            4: 'Wednesday',
            5: 'Thursday',
            6: 'Friday',
            7: 'Saturday'
        }

        today = timezone.localtime(timezone.now()).date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + \
            timedelta(days=6, hours=23, minutes=59, seconds=59)

        task_count_for_weekdays = ProjectProgress.objects.filter(
            completed_at__range=(start_of_week, start_of_week +
                                 timedelta(days=7, hours=23, minutes=59, seconds=59)),
            task_completed=True
        ).annotate(
            weekday=ExtractWeekDay(
                'completed_at', tzinfo=pytz.timezone('Asia/Seoul'))
        ).values('weekday').annotate(count=Count('id'))

        task_count_for_weekdays = {
            weekday_mapping[entry['weekday']]: entry['count']
            for entry in task_count_for_weekdays
        }

        all_weekdays = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']

        task_count_for_weekdays = {
            weekday: task_count_for_weekdays.get(weekday, 0)
            for weekday in all_weekdays
        }

        # todo2: 오늘 날짜의 정보 (날짜와 요일) 구하기
        today_info = {
            'date': now.strftime("%Y년 %m월 %d일"),
            'dayOfWeek': now.strftime('%A')
        }

        today_tasks = ProjectProgress.objects.filter(
            Q(due_date__gte=morning_start) &
            Q(due_date__lt=night_end)
        )

        # Step 1: Initialize a default dictionary to store task counts for each task manager
        task_managers = defaultdict(
            lambda: {'completed_count': 0, 'uncompleted_count': 0})

        # step2 오늘의 업무에 대해 task_manager 와 count 정보를 dict 형식으로 초기화
        for task in today_tasks:
            task_manager = task.task_manager
            if task.current_status == 'completed':
                task_managers[task_manager.username]['completed_count'] += 1
            else:
                task_managers[task_manager.username]['uncompleted_count'] += 1

        # stpe3 task_managers 에 저장된 정보를 다시 list로 만들기
        task_managers_data = []

        for task_manager, counts in task_managers.items():
            task_manager_data = {
                'task_manager': task_manager,
                'uncompleted_count': counts['uncompleted_count'],
                'completed_count': counts['completed_count']
            }
            task_managers_data.append(task_manager_data)

        # Step 4: Sort the task_managers_data list based on the completed_count in descending order
        task_managers_data = sorted(
            task_managers_data, key=lambda x: x['completed_count'], reverse=True)

        response_data = {
            "toal_task_count_for_today":  toal_task_count_for_today,
            "task_count_for_uncompleted_task_until_yesterday": task_count_for_uncompleted_task_until_yesterday,
            "task_count_for_ready": task_count_for_ready,
            "task_count_for_in_progress": task_count_for_in_progress,
            "task_count_for_testing": task_count_for_testing,
            "task_count_for_completed": task_count_for_completed,
            "progress_rate": progress_rate,
            "morning_tasks": TaskSerializerForToday(morning_tasks, many=True).data,
            "afternoon_tasks": TaskSerializerForToday(afternoon_tasks, many=True).data,
            "night_tasks": TaskSerializerForToday(night_tasks, many=True).data,
            'task_count_for_weekdays': task_count_for_weekdays,
            'today_info': today_info,
            'task_managers_data': task_managers_data
        }

        return Response(response_data, status=HTTP_200_OK)


def getStaticsForDailyCompletedTaskCountForMonthForPernalUser(userPk):
    # Get the date a month ago from now
    # Set the timezone to 'Asia/Seoul'
    seoul_tz = pytz.timezone('Asia/Seoul')

    # Get the current time in the 'Asia/Seoul' timezone
    now = datetime.now(seoul_tz)
    print("완료 현황 for User hahahahahahahahahahaha : ", now)

    # Get the date a month ago from now
    one_month_ago = now - timedelta(days=30)

    # Query the database with additional filter condition for the specific user
    user_tasks = ProjectProgress.objects.filter(
        task_manager__pk=userPk,
        current_status=ProjectProgress.TaskStatusChoices.completed,
        completed_at__gte=one_month_ago
    ).annotate(
        date=TruncDate('completed_at')
    ).values('date').annotate(
        myCompletedCount=Count('id')
    ).order_by('date')

    # Query the database for all tasks in the same date range
    all_tasks = ProjectProgress.objects.filter(
        current_status=ProjectProgress.TaskStatusChoices.completed,
        completed_at__gte=one_month_ago
    ).annotate(
        date=TruncDate('completed_at')
    ).values('date').annotate(
        totalCompletedCount=Count('id')
    ).order_by('date')

    print("all_tasks :::::::::::::::::::::::", all_tasks)

    # Format the results to match the format you want
    user_task_data = {task['date'].strftime(
        '%m-%d'): task['myCompletedCount'] for task in user_tasks}
    all_task_data = {task['date'].strftime(
        '%m-%d'): task['totalCompletedCount'] for task in all_tasks}

    # Generate a list of all dates within the last month
    # date_range = pd.date_range(
    #     end=timezone.now().date(), periods=30).to_pydatetime().tolist()
    date_range = pd.date_range(end=now, periods=30).to_pydatetime().tolist()

    all_dates = {date.strftime(
        '%m-%d'): {'myCompletedCount': 0, 'totalCompletedCount': 0} for date in date_range}

    # Merge the task data with all_dates
    for date in all_dates.keys():
        all_dates[date]['myCompletedCount'] = user_task_data.get(date, 0)
        all_dates[date]['totalCompletedCount'] = all_task_data.get(date, 0)

    # Convert the merged data to the desired format
    data = [{'name': date, 'myCompletedCount': count_info['myCompletedCount'],
             'totalCompletedCount': count_info['totalCompletedCount']} for date, count_info in all_dates.items()]
    print("data :::::::::::::::::::", data)

    return data


class TaskStaticsIViewForPersnalUser(APIView):
    def get(self, request, userPk):

        username = User.objects.get(id=userPk).username

        response_data = {
            "username": username,
            "task_count_for_month": []
        }

        staticsForDailyCompletedTaskCountForMonth = getStaticsForDailyCompletedTaskCountForMonthForPernalUser(
            userPk)
        response_data["task_count_for_month"] = staticsForDailyCompletedTaskCountForMonth

        return Response(response_data)


def getStaticsForDailyCompletedTaskCountForMonth():
    # Get the date a month ago from now
    one_month_ago = timezone.now() - timedelta(days=30)

    # Query the database
    tasks = ProjectProgress.objects.filter(
        current_status=ProjectProgress.TaskStatusChoices.completed,
        completed_at__gte=one_month_ago
    ).annotate(
        date=TruncDate('completed_at')
    ).values('date').annotate(
        completedCount=Count('id')
    ).order_by('date')

    # Format the results to match the format you want
    task_data = {task['date'].strftime(
        '%m-%d'): task['completedCount'] for task in tasks}

    # Generate a list of all dates within the last month
    date_range = pd.date_range(
        end=timezone.now().date(), periods=30).to_pydatetime().tolist()
    all_dates = {date.strftime('%m-%d'): 0 for date in date_range}

    # Merge the task data with all_dates
    all_dates.update(task_data)

    # Convert the merged data to the desired format
    data = [{'name': date, 'completedCount': count}
            for date, count in all_dates.items()]

    return data


class DailyCompletedTasks(APIView):
    def get(self, request, format=None):
        # Get the date a month ago from now
        one_month_ago = timezone.now() - timedelta(days=30)

        # Query the database
        tasks = ProjectProgress.objects.filter(
            current_status=ProjectProgress.TaskStatusChoices.completed,
            completed_at__gte=one_month_ago
        ).annotate(
            date=TruncDate('completed_at')
        ).values('date').annotate(
            completedCount=Count('id')
        ).order_by('date')

        # Format the results to match the format you want
        task_data = {task['date'].strftime(
            '%m-%d'): task['completedCount'] for task in tasks}

        # Generate a list of all dates within the last month
        date_range = pd.date_range(
            end=timezone.now().date(), periods=30).to_pydatetime().tolist()
        all_dates = {date.strftime('%m-%d'): 0 for date in date_range}

        # Merge the task data with all_dates
        all_dates.update(task_data)

        # Convert the merged data to the desired format
        data = [{'name': date, 'completedCount': count}
                for date, count in all_dates.items()]

        return Response(data)

# dataForTaskStaticsForIsCompleted
# total_count_for_completed_task


class TaskStaticsIView(APIView):
    def get(self, request):
        task_managers = ProjectProgress.objects.values_list(
            'task_manager', flat=True).distinct()

        response_data = {
            "managers": [],
            "task_count_for_month": []
        }

        for manager in task_managers:
            completed_count_for_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=True).count()
            count_for_testing_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=False, is_testing=True).count()
            uncompleted_count_for_task = ProjectProgress.objects.filter(
                task_manager=manager, task_completed=False, is_testing=False).count()
            total_count_for_uncompleted_task = uncompleted_count_for_task + count_for_testing_task
            total_count_for_completed_task = completed_count_for_task

            total_count_for_task = uncompleted_count_for_task + \
                count_for_testing_task + completed_count_for_task
            task_manager = User.objects.get(pk=manager).username

            manager_data = {
                "task_manager": task_manager,
                "completed_count_for_task": completed_count_for_task,
                "count_for_testing_task": count_for_testing_task,
                "uncompleted_count_for_task": uncompleted_count_for_task,
                "total_count_for_uncompleted_task": total_count_for_uncompleted_task,
                "total_count_for_completed_task": total_count_for_completed_task,
                "total_count_for_task": total_count_for_task
            }
            response_data["managers"].append(manager_data)

            staticsForDailyCompletedTaskCountForMonth = getStaticsForDailyCompletedTaskCountForMonth()
            response_data["task_count_for_month"] = staticsForDailyCompletedTaskCountForMonth

        return Response(response_data)


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


class UpdateForTaskClassificationForChecked(APIView):
    def put(self, request, *args, **kwargs):
        # ex) checkedRowPks 는 [1,2,3,6] ProjectProgress 의 pk
        checked_row_pks = request.data.get('checkedRowPks', [])
        # ex) task_manager 는 ProjectProgress 의 task_manager
        task_classification = request.data.get('task_classification', None)

        print("task_classification:", task_classification)

        # checkedRowPks에 해당하는 ProjectProgress 객체들을 가져옴
        project_progress_list = ProjectProgress.objects.filter(
            pk__in=checked_row_pks)

        # 모든 가져온 ProjectProgress 객체의 task_manager를 selected_manager로 업데이트
        for project_progress in project_progress_list:
            project_progress.task_classification = task_classification
            project_progress.save()

        message = f"Task task_classification updated to {task_classification}."

        return Response({"message": message}, status=HTTP_200_OK)


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
        print("혹시 계속 실행되고 있나?")
        checked_row_pks = request.query_params.get(
            "checkedRowPks", "").split("|")
        checked_row_pks = [int(pk) for pk in checked_row_pks if pk]

        print("체크된 pks for task list1 : ", checked_row_pks)

        pk_list = [int(pk) for pk in checked_row_pks if pk]
        all_project_tasks = ProjectProgress.objects.filter(pk__in=pk_list)

        total_count = all_project_tasks.count()
        serializer = SerializerForUncompletedTaskDetailListForChecked(
            all_project_tasks, many=True)

        data = {
            "total_count": total_count,
            "ProjectProgressList": serializer.data
        }

        return Response(data, status=HTTP_200_OK)


# fix 0603 마감날짜 update 월화수목금토일 단 오늘 이전이면 업데이트 할수 없음


class UpdateViewForTaskDueDateForChecked(APIView):
    def put(self, request):
        # duration_option 값을 가져옵니다.
        duration_option = request.data.get("duration_option")
        # checkedRowPks 값을 가져옵니다.
        checked_row_pks = request.data.get("checkedRowPks")

        print("duration_option : ", duration_option)

        # pk가 checked_row_pks에 포함된 ProjectProgress 모델 인스턴스들의 due_date와 started_at_utc를 업데이트합니다.
        updated_count = 0

        if duration_option == "undetermined":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = None
                    task.started_at_utc = None
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        if duration_option == "noon":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                        timezone.now()).date(), time(hour=12, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
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
                        timezone.now()).date(), time(hour=18, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
                    # started_at_utc 필드를 서버 시간 기준으로 현재 시간으로 업데이트합니다.
                    task.started_at_utc = timezone.localtime(
                        timezone.now()).astimezone(timezone.utc)
                    task.save()
                    updated_count += 1
                except ProjectProgress.DoesNotExist:
                    pass

        elif duration_option == "night":
            for pk in checked_row_pks:
                try:
                    task = ProjectProgress.objects.get(pk=pk)
                    task.due_date = timezone.make_aware(datetime.combine(timezone.localtime(
                        timezone.now()).date(), time(hour=23, minute=59)))  # 서버 시간 기준으로 오늘 오후 7시로 설정
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

# DeleteCompletedTasksForChecked


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

    sorted_task_managers_info = sorted(
        task_managers_info, key=lambda x: x['task_count'], reverse=True)
    return sorted_task_managers_info


def get_writers_info_for_in_prgress():
    print("get_writers_info_for_in_prgress !!!!!!!!! ")
    task_manager_counts = ProjectProgress.objects.filter(in_progress=True, task_completed=False).values(
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

    sorted_task_managers_info = sorted(
        task_managers_info, key=lambda x: x['task_count'], reverse=True)
    return sorted_task_managers_info


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
                # original_task = self.get_object(taskPk)
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
                serializer = TestSerializerForOneTask(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")


class CreateViewForTestForExtraTask(APIView):

    print("test 추가 요청 22 !!!!!!!!!!")

    def get_object(self, taskPk):
        print("taskPk :::::::::::::: ", taskPk)
        try:
            return ExtraTask.objects.get(pk=taskPk)
        except ExtraTask.DoesNotExist:
            raise NotFound

    def post(self, request, taskPk):
        print("post 요청 받음 !!!!!!!!!!!!!!")
        serializer = CreateTestSerializerForExtraTask(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                original_task = self.get_object(taskPk)
                test_for_task = serializer.save(original_task=original_task)
                serializer = CreateTestSerializerForExtraTask(test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("eeeeeeeeeeeeee : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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

    def get(self, request):
        extra_tasks = ExtraTask.objects.all()
        serializer = ExtraTasksSerializer(extra_tasks, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

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

# ready = ("ready", "준비")
# in_progress = ("in_progress", "작업중")
# testing = ("testing", "테스트중")
# completed = ("completed", "완료")


class UpdateViewForExtraTaskProgressStatus(APIView):
    def get_object(self, pk):
        try:
            print("pk check at get_object : ", pk)
            return ExtraTask.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        print("request.data : ", request.data)
        status_for_update = request.data.get('task_status')

        extra_task = self.get_object(pk)
        extra_task.task_status = status_for_update

        if (status_for_update == "in_progress"):
            extra_task.started_at = timezone.now()
        elif (status_for_update == "ready"):
            extra_task.started_at = None

        if (status_for_update == "completed"):
            if (extra_task.started_at == None):
                extra_task.started_at = timezone.now()
            extra_task.completed_at = timezone.now()
        else:
            extra_task.completed_at = None

        try:
            extra_task.save()
            message = "extra task update 성공"
            print("update result : ", extra_task)

            return Response({"message": message}, status=HTTP_200_OK)
        except Exception as e:
            print("Error during extra task update:", str(e))
            return Response({"message": "extra task update 실패"}, status=HTTP_400_BAD_REQUEST)


class ExtraTaskDetail(APIView):
    def get_object(self, pk):
        try:
            print("pk check at get_object : ", pk)
            return ExtraTask.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        extra_task = self.get_object(pk)
        print("request.data : ", request.data)  # request.data 출력

        serializer = ExtraTasksDetailSerializer(extra_task)
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, pk):
        print("delete request check !!")
        extra_task = self.get_object(pk)

        # TODO: 로그인 안했으면 로그인 유저만 삭제 가능 메세지와 함께 response
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_401_UNAUTHORIZED)

        # TODO: extra_task.task_manager와 request.user가 같지 않으면 삭제 권한 없음 메세지와 함께 response
        if extra_task.task_manager != request.user:
            return Response({"message": "삭제 권한이 없습니다."}, status=HTTP_403_FORBIDDEN)

        # extra_task가 존재할 경우 삭제하고 삭제 완료 메시지와 함께 response
        extra_task.delete()
        return Response({"message": "부가 업무를 삭제하였습니다."}, status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        print("request.data : ", request.data)
        extra_task = self.get_object(pk)

        # 업데이트할 필드명과 값을 직접 설정
        task_manager_id = request.data.get('task_manager')
        print("task_manager_id :::::::::::::::::", task_manager_id)
        print("task_description  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ",
              request.data.get('task_description'))

        task_manager = User.objects.get(pk=task_manager_id)
        extra_task.task_manager = task_manager

        extra_task.task = request.data.get('task')
        extra_task.task_description = request.data.get('task_description')
        extra_task.task_status = request.data.get('task_status')

        try:
            extra_task.save()
            message = "extra task update 성공"
            print("update result : ", extra_task)

            return Response({"message": message}, status=HTTP_200_OK)
        except Exception as e:
            print("Error during extra task update:", str(e))
            return Response({"message": "extra task update 실패"}, status=HTTP_400_BAD_REQUEST)


# 0414
class TaskStatusListView(APIView):
    one_month_ago = timezone.now() - timedelta(days=30)
    date_from = ""
    all_tasks = ProjectProgress.objects.all()

    def get_all_tasks(self, request):

        task_manager = ""
        date_range = request.query_params.get('dateRange', 'thisMonth')

        task_manager = request.query_params.get(
            'taskManagerForFiltering', '')
        importance = request.query_params.get('importance', 1)

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
            evening = time(hour=19, minute=1, second=0)
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


# class UncompletedTaskListView(APIView):
#     totalCountForTask = 0  # total_count 계산
#     task_number_for_one_page = 10  # 1 페이지에 몇개씩
#     all_uncompleted_project_task_list = []
#     completed_project_task_list_for_current_page = []
#     user_for_search = ""

#     def get(self, request):
#         response_data = {}
#         try:
#             page = request.query_params.get("page", 1)
#             page = int(page)

#             period_option = request.query_params.get(
#                 "selectedPeriodOptionForUncompletedTaskList", "all")
#             task_status_option = request.query_params.get(
#                 "task_status_for_search", "")
#             self.user_for_search = request.query_params.get(
#                 "username_for_search", "")
#             due_date_option_for_filtering = request.query_params.get(
#                 "due_date_option_for_filtering", "")
#             rating_for_filter_option = request.query_params.get(
#                 "rating_for_filter_option", "")
#             isForUrgent = request.query_params.get(
#                 "isForUrgent", False)
#             checkForCashPrize = request.query_params.get(
#                 "checkForCashPrize", False)
#             groupByOption = request.query_params.get(
#                 "groupByOption", "")
#             is_task_due_date_has_passed = request.query_params.get(
#                 "is_task_due_date_has_passed", False)

#             if period_option == "all":
#                 self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
#                     task_completed=False).order_by('-created_at')
#             elif period_option == "within_a_week":
#                 one_week_ago = datetime.now() - timedelta(days=7)
#                 self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
#                     task_completed=False, created_at__gte=one_week_ago).order_by('-created_at')
#             elif period_option == "within_a_month":
#                 one_month_ago = datetime.now() - timedelta(days=30)
#                 self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
#                     task_completed=False, created_at__gte=one_month_ago).order_by('-created_at')
#             elif period_option == "over_a_month_ago":
#                 one_month_ago = datetime.now() - timedelta(days=30)
#                 self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
#                     task_completed=False, created_at__lt=one_month_ago).order_by('-created_at')

#             if self.user_for_search == "":
#                 count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
#                     task_completed=False).count()
#             else:
#                 count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
#                     task_completed=False, task_manager__username=self.user_for_search).count()

#             if is_task_due_date_has_passed == "true":
#                 current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
#                 count_for_all_uncompleted_project_task_list = self.all_uncompleted_project_task_list.filter(
#                     due_date__lt=current_datetime, due_date__isnull=False).count()

#             self.totalCountForTask = math.trunc(
#                 count_for_all_uncompleted_project_task_list)

#             start = (page - 1) * self.task_number_for_one_page
#             end = start + self.task_number_for_one_page

#             if self.user_for_search != "":
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     task_manager__username=self.user_for_search)
#             else:
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
#                     start:end]

#             if task_status_option != "":
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     current_status=task_status_option)

#             if due_date_option_for_filtering == "undecided":
#                 noon = time(hour=12, minute=10, second=0)
#                 deadline = datetime.combine(datetime.today(), noon)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date=None)

#             if due_date_option_for_filtering == "until-yesterday":
#                 morning = time(hour=0, minute=0, second=0)
#                 deadline = datetime.combine(datetime.today(), morning)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lt=deadline)

#             if due_date_option_for_filtering == "until-noon":
#                 noon = time(hour=12, minute=10, second=0)
#                 deadline = datetime.combine(datetime.today(), noon)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-evening":
#                 print("due_date_option_for_filtering !!!!!!!!!!!! ")
#                 evening = time(hour=19, minute=10, second=0)
#                 deadline = datetime.combine(datetime.today(), evening)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-night":
#                 print("due_date_option_for_filtering !!!!!!!!!!!! ")
#                 evening = time(hour=23, minute=59, second=59)
#                 deadline = datetime.combine(datetime.today(), evening)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-tomorrow":
#                 print("due_date_option_for_filtering !!!!!!!!!!!! ")
#                 tomorrow = datetime.today() + timedelta(days=1)
#                 evening = time(hour=19, minute=10, second=0)
#                 deadline = datetime.combine(tomorrow, evening)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-the-day-after-tomorrow":
#                 print("due_date_option_for_filtering tomorrow !!!!!!!!!!!! ")
#                 tomorrow = datetime.today() + timedelta(days=2)
#                 evening = time(hour=19, minute=10, second=0)
#                 deadline = datetime.combine(tomorrow, evening)
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-this-week":
#                 print("due_date_option_for_filtering this week !!!!!!!!!!!! ")
#                 today = datetime.today()
#                 last_day_of_week = today + timedelta(days=(6 - today.weekday()))
#                 deadline = datetime.combine(
#                     last_day_of_week, time(hour=23, minute=59, second=59))
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if due_date_option_for_filtering == "until-this-month":
#                 print("due_date_option_for_filtering this month !!!!!!!!!!!! ")
#                 today = datetime.today()
#                 # 이번 달의 마지막 날짜 계산
#                 last_day_of_month = datetime(
#                     today.year, today.month, 1) + timedelta(days=32)
#                 last_day_of_month = last_day_of_month.replace(
#                     day=1) - timedelta(days=1)
#                 # 이번 달 마지막 날짜의 오후 11시 59분 59초까지
#                 deadline = datetime.combine(
#                     last_day_of_month, time(hour=23, minute=59, second=59))
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lte=deadline)

#             if rating_for_filter_option != "":
#                 if int(rating_for_filter_option) > 0:
#                     print("rating_for_filter_option : ", rating_for_filter_option)
#                     self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                         importance=rating_for_filter_option)

#             if isForUrgent == "true":
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     is_task_for_urgent=True)
#             if checkForCashPrize == "true":
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     is_task_for_cash_prize=True)

#             if groupByOption != "":
#                 if groupByOption == "member":
#                     self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.order_by(
#                         'task_manager')
#                 if groupByOption == "importance":
#                     self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.order_by(
#                         'importance')

#             if is_task_due_date_has_passed == "true":
#                 # todo due_date 가 지금 시간 보다 과거인것들 검색 (현지 시간 기준)

#                 current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
#                 self.uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
#                     due_date__lt=current_datetime, due_date__isnull=False
#                 )

#             serializer = ProjectProgressListSerializer(
#                 self.uncompleted_project_task_list_for_current_page, many=True)

#             if self.user_for_search == "":
#                 current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
#                 count_for_ready = self.all_uncompleted_project_task_list.filter(
#                     in_progress=False).count()
#                 count_for_in_progress = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=False, task_completed=False).count()
#                 count_for_in_testing = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=True, task_completed=False).count()
#                 count_for_duedate_passed = self.all_uncompleted_project_task_list.filter(
#                     due_date__lt=current_datetime, task_completed=False).count()

#             else:
#                 current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
#                 serializer = ProjectProgressListSerializer(
#                     self.uncompleted_project_task_list_for_current_page, many=True)
#                 count_for_ready = self.all_uncompleted_project_task_list.filter(
#                     in_progress=False, task_manager__username=self.user_for_search).count()
#                 count_for_in_progress = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=False, task_completed=False, task_manager__username=self.user_for_search).count()
#                 count_for_in_testing = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=True, task_completed=False, task_manager__username=self.user_for_search).count()
#                 count_for_duedate_passed = self.all_uncompleted_project_task_list.filter(
#                     due_date__lt=current_datetime, task_completed=False, task_manager__username=self.user_for_search).count()

#             print("is_task_due_date_has_passed ::::::::::::::: ",
#                 is_task_due_date_has_passed)

#             if is_task_due_date_has_passed == "true":
#                 current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴

#                 count_for_ready = self.all_uncompleted_project_task_list.filter(
#                     in_progress=False, due_date__lt=current_datetime, due_date__isnull=False).count()
#                 count_for_in_progress = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=False, task_completed=False, due_date__lt=current_datetime, due_date__isnull=False).count()
#                 count_for_in_testing = self.all_uncompleted_project_task_list.filter(
#                     in_progress=True, is_testing=True, task_completed=False, due_date__lt=current_datetime, due_date__isnull=False).count()

#             # 리스트 직렬화
#             data = serializer.data

#             # 작성자 목록
#             writers_info = get_writers_info(complete_status=False)

#             # 오늘까지인 task 총 개수
#             deadline = datetime.combine(
#                 datetime.today(), time(hour=23, minute=59, second=59))
#             # fix
#             # 서울 시간대 설정
#             timezone = pytz.timezone('Asia/Seoul')

#             # 서울 시간으로 오늘의 시작과 끝 시간 계산
#             today_start = timezone.localize(
#                 datetime.combine(date.today(), time.min))
#             today_end = timezone.localize(datetime.combine(date.today(), time.max))

#             total_task_count_for_today = ProjectProgress.objects.filter(
#                 due_date__range=(today_start, today_end)).count()

#             completed_task_count_for_today = ProjectProgress.objects.filter(
#                 task_completed=True, due_date__range=(today_start, today_end)).count()

#             achievement_rate_for_today = 0  # 기본값으로 0 설정

#             if total_task_count_for_today != 0:
#                 achievement_rate_for_today = (
#                     completed_task_count_for_today / total_task_count_for_today) * 100
#                 achievement_rate_for_today = round(achievement_rate_for_today)

#             current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
#             task_count_for_due_date_passed = self.all_uncompleted_project_task_list.filter(
#                 due_date__lt=current_datetime, due_date__isnull=False).count()

#             response_data = {
#                 "writers_info": writers_info,
#                 "ProjectProgressList": data,
#                 "count_for_ready": count_for_ready,
#                 "count_for_in_progress": count_for_in_progress,
#                 "count_for_in_testing": count_for_in_testing,
#                 "count_for_duedate_passed": count_for_duedate_passed,
#                 "totalPageCount": self.totalCountForTask,
#                 "task_number_for_one_page": self.task_number_for_one_page,
#                 "total_task_count_for_today": total_task_count_for_today,
#                 "completed_task_count_for_today": completed_task_count_for_today,
#                 "achievement_rate_for_today": achievement_rate_for_today,
#                 "task_count_for_due_date_passed": task_count_for_due_date_passed
#             }

#         except ValueError:
#             page = 1

#         except Exception as e:  # 에러 처리를 위해 Exception으로 변경
#             # ObjectDoesNotExist 에러가 발생한 경우
#             error_message = str(e)  # 에러 메시지를 문자열로 변환
#             response_data = {"error": error_message}
#             return Response(response_data, status=HTTP_400_BAD_REQUEST)

#         return Response(response_data, status=HTTP_200_OK)

# 필요한거 진행중인 업무 리스트, 개수 , 유저별
class InProgressTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 10  # 1 페이지에 몇 개씩
    all_uncompleted_project_task_list = []
    user_for_search = ""
    order_by_field = "id"

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            period_option = request.query_params.get(
                "selectedPeriodOptionForUncompletedTaskList", "all")

            task_status_for_filter = request.query_params.get(
                "task_status_for_filter", "")
            due_date_option_for_filtering = request.query_params.get(
                "due_date_option_for_filtering", "")
            self.user_for_search = request.query_params.get(
                "username_for_search", "")
            isForUrgent = request.query_params.get("isForUrgent", False)

            checkForCashPrize = request.query_params.get(
                "checkForCashPrize", False)

            groupByOption = request.query_params.get(
                "groupByOption", "")

            is_task_due_date_has_passed = request.query_params.get(
                "is_task_due_date_has_passed", False)

            print("is_task_due_date_has_passed :::::::::::::",
                  is_task_due_date_has_passed)

            # 필터링 조건을 간소화
            filter_params = {"task_completed": False, "in_progress": True}

            # print("groupByOption ::::::::::::::::::", groupByOption)

            if groupByOption == "member":
                self.order_by_field = 'task_manager'
            elif groupByOption == "importance":
                self.order_by_field = '-importance'

            if period_option == "within_a_week":
                filter_params["created_at__gte"] = datetime.now() - \
                    timedelta(days=7)
            elif period_option == "within_a_month":
                filter_params["created_at__gte"] = datetime.now() - \
                    timedelta(days=30)
            elif period_option == "over_a_month_ago":
                filter_params["created_at__lt"] = datetime.now() - \
                    timedelta(days=30)

            if self.user_for_search:
                filter_params["task_manager__username"] = self.user_for_search

            if isForUrgent == "true":
                filter_params["is_task_for_urgent"] = True

            if checkForCashPrize == "true":
                filter_params["is_task_for_cash_prize"] = True

            if task_status_for_filter:
                filter_params["current_status"] = task_status_for_filter
            print("due_date_option_for_filtering :::::::::::::",
                  due_date_option_for_filtering)

            if is_task_due_date_has_passed == "true":
                current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
                filter_params["due_date__lt"] = current_datetime
                filter_params["due_date__isnull"] = False

            if due_date_option_for_filtering == "until-yesterday":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(0, 0, 0))

            elif due_date_option_for_filtering == "until-noon":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(12, 10, 0))

            if due_date_option_for_filtering == "until-evening":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(19, 10, 0))

            if due_date_option_for_filtering == "until-night":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(23, 59, 59))

            if due_date_option_for_filtering == "until-tomorrow":
                tomorrow = datetime.today() + timedelta(days=1)
                evening = time(hour=19, minute=10, second=0)
                filter_params["due_date__lt"] = datetime.combine(
                    tomorrow, evening)

            if due_date_option_for_filtering == "until-the-day-after-tomorrow":
                day_afoter_tomorrow = datetime.today() + timedelta(days=2)
                evening = time(hour=19, minute=10, second=0)
                filter_params["due_date__lt"] = datetime.combine(
                    day_afoter_tomorrow, evening)

            if due_date_option_for_filtering == "until-this-week":
                print("due_date_option_for_filtering this week !!!!!!!!!!!! ")
                today = datetime.today()
                last_day_of_week = today + \
                    timedelta(days=(6 - today.weekday()))
                filter_params["due_date__lt"] = datetime.combine(
                    last_day_of_week, time(hour=23, minute=59, second=59))

            if due_date_option_for_filtering == "until-this-month":
                #  print("due_date_option_for_filtering this month !!!!!!!!!!!! ")
                today = datetime.today()
                # 이번 달의 마지막 날짜 계산
                last_day_of_month = datetime(
                    today.year, today.month, 1) + timedelta(days=32)
                last_day_of_month = last_day_of_month.replace(
                    day=1) - timedelta(days=1)
                # 이번 달 마지막 날짜의 오후 11시 59분 59초까지
                filter_params["due_date__lt"] = datetime.combine(
                    last_day_of_month, time(hour=23, minute=59, second=59))

            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                **filter_params).order_by('-created_at').order_by(self.order_by_field)

            self.totalCountForTask = self.all_uncompleted_project_task_list.count()
            start = (page - 1) * self.task_number_for_one_page
            end = start + self.task_number_for_one_page

            if self.user_for_search:
                uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                    task_manager__username=self.user_for_search)
            else:
                uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
                    start:end]

            serializer = ProjectProgressListSerializer(
                uncompleted_project_task_list_for_current_page, many=True)

            response_data = {
                "writers_info": get_writers_info_for_in_prgress(),
                "ProjectProgressList": serializer.data,
                "totalPageCount": self.totalCountForTask,
                "task_number_for_one_page": self.task_number_for_one_page,
                "count_for_in_progress": self.all_uncompleted_project_task_list.filter(in_progress=True, is_testing=False, task_completed=False).count(),
                "count_for_in_testing": self.all_uncompleted_project_task_list.filter(in_progress=True, is_testing=True, task_completed=False).count(),
                "task_count_for_due_date_passed": self.get_task_count_for_due_date_passed(),
                "count_for_duedate_passed": self.all_uncompleted_project_task_list.filter(due_date__lt=datetime.now(), task_completed=False).count(),
                # "count_for_ready": self.all_uncompleted_project_task_list.filter(in_progress=False).count(),
                "total_task_count_for_today": self.get_total_task_count_for_today(),
                "completed_task_count_for_today": self.get_completed_task_count_for_today(),
                "achievement_rate_for_today": self.get_achievement_rate_for_today(),
            }

            return Response(response_data, status=HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            response_data = {"error": error_message}
            return Response(response_data, status=HTTP_400_BAD_REQUEST)

    def get_total_task_count_for_today(self):
        today_start, today_end = self.get_today_start_and_end()
        return ProjectProgress.objects.filter(due_date__range=(today_start, today_end)).count()

    def get_completed_task_count_for_today(self):
        today_start, today_end = self.get_today_start_and_end()
        return ProjectProgress.objects.filter(task_completed=True, due_date__range=(today_start, today_end)).count()

    def get_achievement_rate_for_today(self):
        total_task_count_for_today = self.get_total_task_count_for_today()
        if total_task_count_for_today == 0:
            return 0
        completed_task_count_for_today = self.get_completed_task_count_for_today()
        return round((completed_task_count_for_today / total_task_count_for_today) * 100)

    def get_task_count_for_due_date_passed(self):
        current_datetime = datetime.now()
        count = self.all_uncompleted_project_task_list.filter(
            due_date__lt=current_datetime, due_date__isnull=False).count()
        return count if count is not None else 0

    def get_today_start_and_end(self):
        timezone = pytz.timezone('Asia/Seoul')
        today_start = timezone.localize(
            datetime.combine(date.today(), time.min))
        today_end = timezone.localize(datetime.combine(date.today(), time.max))
        return today_start, today_end


class UncompletedTaskListView(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 10  # 1 페이지에 몇 개씩
    all_uncompleted_project_task_list = []
    user_for_search = ""
    order_by_field = "id"

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            period_option = request.query_params.get(
                "selectedPeriodOptionForUncompletedTaskList", "all")

            task_status_for_filter = request.query_params.get(
                "task_status_for_filter", "")
            due_date_option_for_filtering = request.query_params.get(
                "due_date_option_for_filtering", "")
            self.user_for_search = request.query_params.get(
                "username_for_search", "")
            isForUrgent = request.query_params.get("isForUrgent", False)

            checkForCashPrize = request.query_params.get(
                "checkForCashPrize", False)

            groupByOption = request.query_params.get(
                "groupByOption", "")

            is_task_due_date_has_passed = request.query_params.get(
                "is_task_due_date_has_passed", False)

            # 필터링 조건을 간소화
            filter_params = {"in_progress": False, "task_completed": False}

            print("groupByOption ::::::::::::::::::", groupByOption)

            if groupByOption == "member":
                self.order_by_field = 'task_manager'
            elif groupByOption == "importance":
                self.order_by_field = '-importance'

            if period_option == "within_a_week":
                filter_params["created_at__gte"] = datetime.now() - \
                    timedelta(days=7)
            elif period_option == "within_a_month":
                filter_params["created_at__gte"] = datetime.now() - \
                    timedelta(days=30)
            elif period_option == "over_a_month_ago":
                filter_params["created_at__lt"] = datetime.now() - \
                    timedelta(days=30)

            if self.user_for_search:
                filter_params["task_manager__username"] = self.user_for_search

            if isForUrgent == "true":
                filter_params["is_task_for_urgent"] = True

            if checkForCashPrize == "true":
                filter_params["is_task_for_cash_prize"] = True

            if task_status_for_filter:
                filter_params["current_status"] = task_status_for_filter

            print("due_date_option_for_filtering :::::::::::::",
                  due_date_option_for_filtering)

            if is_task_due_date_has_passed == "true":
                current_datetime = datetime.now()  # 현재 시간을 현지 시간 기준으로 가져옴
                filter_params["due_date__lt"] = current_datetime
                filter_params["due_date__isnull"] = False

            if due_date_option_for_filtering == "until-yesterday":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(0, 0, 0))

            elif due_date_option_for_filtering == "until-noon":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(12, 10, 0))

            if due_date_option_for_filtering == "until-evening":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(19, 10, 0))

            if due_date_option_for_filtering == "until-night":
                filter_params["due_date__lt"] = datetime.combine(
                    date.today(), time(23, 59, 59))

            if due_date_option_for_filtering == "until-tomorrow":
                tomorrow = datetime.today() + timedelta(days=1)
                evening = time(hour=19, minute=10, second=0)
                filter_params["due_date__lt"] = datetime.combine(
                    tomorrow, evening)

            if due_date_option_for_filtering == "until-the-day-after-tomorrow":
                day_afoter_tomorrow = datetime.today() + timedelta(days=2)
                evening = time(hour=19, minute=10, second=0)
                filter_params["due_date__lt"] = datetime.combine(
                    day_afoter_tomorrow, evening)

            if due_date_option_for_filtering == "until-this-week":
                print("due_date_option_for_filtering this week !!!!!!!!!!!! ")
                today = datetime.today()
                last_day_of_week = today + \
                    timedelta(days=(6 - today.weekday()))
                filter_params["due_date__lt"] = datetime.combine(
                    last_day_of_week, time(hour=23, minute=59, second=59))

            if due_date_option_for_filtering == "until-this-month":
                #  print("due_date_option_for_filtering this month !!!!!!!!!!!! ")
                today = datetime.today()
                # 이번 달의 마지막 날짜 계산
                last_day_of_month = datetime(
                    today.year, today.month, 1) + timedelta(days=32)
                last_day_of_month = last_day_of_month.replace(
                    day=1) - timedelta(days=1)
                # 이번 달 마지막 날짜의 오후 11시 59분 59초까지
                filter_params["due_date__lt"] = datetime.combine(
                    last_day_of_month, time(hour=23, minute=59, second=59))

            self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
                **filter_params).order_by('-created_at').order_by(self.order_by_field)

            self.totalCountForTask = self.all_uncompleted_project_task_list.count()
            start = (page - 1) * self.task_number_for_one_page
            end = start + self.task_number_for_one_page

            if self.user_for_search:
                uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list.filter(
                    task_manager__username=self.user_for_search)
            else:
                uncompleted_project_task_list_for_current_page = self.all_uncompleted_project_task_list[
                    start:end]

            serializer = ProjectProgressListSerializer(
                uncompleted_project_task_list_for_current_page, many=True)

            response_data = {
                "writers_info": get_writers_info(complete_status=False),
                "ProjectProgressList": serializer.data,
                "count_for_ready": self.all_uncompleted_project_task_list.filter(in_progress=False).count(),
                # "count_for_in_progress": self.all_uncompleted_project_task_list.filter(in_progress=True, is_testing=False, task_completed=False).count(),
                # "count_for_in_testing": self.all_uncompleted_project_task_list.filter(in_progress=True, is_testing=True, task_completed=False).count(),
                "count_for_duedate_passed": self.all_uncompleted_project_task_list.filter(due_date__lt=datetime.now(), task_completed=False).count(),
                "totalPageCount": self.totalCountForTask,
                "task_number_for_one_page": self.task_number_for_one_page,
                "total_task_count_for_today": self.get_total_task_count_for_today(),
                "completed_task_count_for_today": self.get_completed_task_count_for_today(),
                "achievement_rate_for_today": self.get_achievement_rate_for_today(),
                "task_count_for_due_date_passed": self.get_task_count_for_due_date_passed(),
            }

            return Response(response_data, status=HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            response_data = {"error": error_message}
            return Response(response_data, status=HTTP_400_BAD_REQUEST)

    def get_total_task_count_for_today(self):
        today_start, today_end = self.get_today_start_and_end()
        return ProjectProgress.objects.filter(due_date__range=(today_start, today_end)).count()

    def get_completed_task_count_for_today(self):
        today_start, today_end = self.get_today_start_and_end()
        return ProjectProgress.objects.filter(task_completed=True, due_date__range=(today_start, today_end)).count()

    def get_achievement_rate_for_today(self):
        total_task_count_for_today = self.get_total_task_count_for_today()
        if total_task_count_for_today == 0:
            return 0
        completed_task_count_for_today = self.get_completed_task_count_for_today()
        return round((completed_task_count_for_today / total_task_count_for_today) * 100)

    def get_task_count_for_due_date_passed(self):
        current_datetime = datetime.now()
        count = self.all_uncompleted_project_task_list.filter(
            due_date__lt=current_datetime, due_date__isnull=False).count()
        return count if count is not None else 0

    def get_today_start_and_end(self):
        timezone = pytz.timezone('Asia/Seoul')
        today_start = timezone.localize(
            datetime.combine(date.today(), time.min))
        today_end = timezone.localize(datetime.combine(date.today(), time.max))
        return today_start, today_end


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
                task_completed=True).order_by('-completed_at', '-created_at')
        elif period_option == "within_a_week":
            one_week_ago = datetime.now() - timedelta(days=7)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__gte=one_week_ago).order_by('-completed_at', '-created_at')
        elif period_option == "within_a_month":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__gte=one_month_ago).order_by('-completed_at', '-created_at')
        elif period_option == "over_a_month_ago":
            one_month_ago = datetime.now() - timedelta(days=30)
            self.all_completed_project_task_list = ProjectProgress.objects.filter(
                task_completed=True, created_at__lt=one_month_ago).order_by('-completed_at', '-created_at')

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
        serializer = CompletedTaskSerializer(
            self.completed_project_task_list_for_current_page, many=True)
        data = serializer.data

        # fix 0605
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


due_date_mapping = {
    'this-morning': timezone.now().replace(hour=0, minute=0, ),
    'this-evening': timezone.now().replace(hour=19, minute=0),
    'this-night': timezone.now().replace(hour=0, minute=0) + timedelta(days=1),
    'tomorrow': timezone.now().replace(hour=12, minute=0) + timedelta(days=1),
    'day-after-tomorrow': timezone.now().replace(hour=12, minute=0) + timedelta(days=2),
    'this-week': timezone.now().replace(hour=12, minute=0) + timedelta(days=7 - timezone.now().weekday()),
    'this-month': timezone.now().replace(day=1, hour=12, minute=0) + timedelta(days=32 - timezone.now().day),
}


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
        due_date_option = request.data.get('due_date_option')
        print("due_date_option :::::::::::::::::::::::: ",
              due_date_option)    # this-evening

        valid_options = ['morning_tasks', 'afternoon_tasks', 'night_tasks']
        if due_date_option not in valid_options:
            due_date_option = 'afternoon_tasks'

        serializer = CreateProjectProgressSerializer(data=request.data)
        if serializer.is_valid():
            task_manager = User.objects.get(pk=request.data['task_manager'])

            project_progress = serializer.save(
                task_manager=task_manager, due_date_option=due_date_option)

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
        # todo1

        if project_task.task_completed:
            message = "완료에서 비완료로 update"
            project_task.task_completed = False
            project_task.current_status = "testing"
            project_task.completed_at = None

            try:
                task_log_for_delete = TaskLog.objects.get(
                    taskPk=project_task.id)
            except TaskLog.DoesNotExist:
                task_log_for_delete = None

            if task_log_for_delete:
                time_distance_for_team_task_for_delete_row = task_log_for_delete.time_distance_for_team_task
                next_task_log = TaskLog.objects.filter(
                    id__gt=task_log_for_delete.id).first()
                before_task_log = TaskLog.objects.filter(
                    id__lt=task_log_for_delete.id).last()
                print("next_task_log ::::::::::::::::::::::::::::", next_task_log,
                      "before_task_log ::::::::::::::::::::::::::::", before_task_log)
                task_log_for_delete.delete()

                if next_task_log:
                    next_task_log.time_distance_for_team_task += time_distance_for_team_task_for_delete_row
                    next_task_log.save()

        else:
            message = "비완료에서 완료로 update"

            # # 현재 날짜 및 시간을 가져옵니다.
            # now = timezone.now()

            # # 현재 날짜의 자정을 계산합니다.
            # today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

            # if project_task.due_date < today_midnight:
            #     return Response({"message": "Due date has passed! if you want task complete update due date is necessary !"})
            # else:
            #     print("그대로 진행 !!!!!!!!!")
            #     print("project_task.due_date : ", project_task.due_date)
            #     print("today_midnight : ", today_midnight)

            # 서울 시간대로 현재 날짜 및 시간을 가져옵니다.
            seoul_timezone = pytz.timezone('Asia/Seoul')
            now = datetime.now(seoul_timezone)

            # 현재 날짜의 자정 (00시 00분 00초)를 계산합니다.
            today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

            if project_task.due_date < today_midnight:
                return Response({"message": "Due date has passed! if you want task complete update due date is necessary !"})
            else:
                print("그대로 진행 !!!!!!!!!")
                print("project_task.due_date : ", project_task.due_date)
                print("today_midnight : ", today_midnight)

            project_task.task_completed = True
            project_task.current_status = "completed"

            # project_task.due_date = 오늘 18시 59분 

            new_completed_at = timezone.localtime()
            project_task.completed_at = new_completed_at  # 현재 시간 저장

            seoul_tz = pytz.timezone('Asia/Seoul')

            before_task_log = TaskLog.objects.filter(
                taskPk__lt=project_task.id,
            ).order_by('-taskPk').first()

            if before_task_log:
                current_time = timezone.localtime()
                time_difference = current_time - before_task_log.completed_at
                interval_between_team_task = time_difference.total_seconds()
            else:
                # 직전에 생성된 업무가 없으면 interval_between_team_task를 0으로 설정
                interval_between_team_task = 0

            if before_task_log and before_task_log.writer == project_task.task_manager:
                current_time = timezone.localtime()
                time_difference_for_my_task = current_time - before_task_log.completed_at
                interval_between_my_task = time_difference_for_my_task.total_seconds()

            else:
                # 생성하려는 업무 바로 이전에 생성한 업무가 없거나 writer가 다르면 시간 차이를 0으로 설정
                interval_between_my_task = 0

            task_log = TaskLog.objects.create(
                original_task=project_task,
                taskPk=project_task.id,
                writer=project_task.task_manager,
                task=project_task.task,
                # todo 11 생성하려는 업무 바로 이전에 생성한 업무가 존재할 경우 시간차(현재 시간 - 생성하려는 업무 바로 이전에 생성한 업무)를 초 단위로 interval_between_team_task에 저장
                time_distance_for_team_task=interval_between_team_task,
                # todo 22 생성하려는 업무 바로 이전에 생성한 업무가 존재하면서 동시에 writer = project_task.task_manager 일 경우
                # time_distance_for_my_task 에 시간 차이(현재 시간 - 생성하려는 업무 바로 이전에 생성한 업무가 존재하면서 동시에 writer = project_task.task_manager 인 업무)를 초 단위로 저장
                time_distance_for_my_task=interval_between_my_task,


                # todo 22 생성하려는 업무 바로 이전에 생성한 업무가 존재하면서 동시에 writer = project_task.task_manager 일 경우
                # time_distance_for_my_task 에 시간 차이(현재 시간 - 생성하려는 업무 바로 이전에 생성한 업무가 존재하면서 동시에 writer = project_task.task_manager 인 업무) 저장
                completed_at=timezone.now().astimezone(pytz.timezone('Asia/Seoul')),
                completed_at_formatted=timezone.now().astimezone(
                    seoul_tz).strftime("%m월 %d일 %H시 %M분")
            )
            task_log.save()

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


class update_task_for_is_task_for_urgent(APIView):
    def get_object(self, pk):
        try:
            return ProjectProgress.objects.get(pk=pk)
        except ProjectProgress.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        message = ""
        print("put 요청 확인")
        project_task = self.get_object(pk)

        if project_task.is_task_for_urgent:
            message = "긴급 업무 대상에서 비긴급 업무로 update"
            project_task.is_task_for_urgent = False
            project_task.cash_prize = 0

        else:
            message = "비긴급 업무 대상에서 긴급 업무로 update"
            project_task.is_task_for_urgent = True

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
        score_by_tester = request.data.get('score_by_tester', 0)
        cashInfoForUpdate = request.data.get('cashInfoForUpdate', 0)
        username = request.data.get('username')
        print("username :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::", username)
        print("score_by_tester :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::", score_by_tester)
        project_task.score_by_tester = score_by_tester

        # 유저 모델 조회
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=HTTP_404_NOT_FOUND)

        # cash에 score_by_tester 업데이트
        user.cash = user.cash + cashInfoForUpdate
        user.save()

        if (cashInfoForUpdate > 0):
            cash_message = cashInfoForUpdate, "원 추가"
        else:
            cash_message = cashInfoForUpdate, "원"

        message = f"{score_by_tester} 점으로 task score update {username} 의 cash update : {cash_message}"

        project_task.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=HTTP_200_OK)


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
        due_date_str = request.data.get("due_date")
        print("due_date ::::::::: ", due_date_str)

        # 문자열을 datetime 객체로 변환하고 시간대 정보 추가
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            # 시간대 정보 추가
            due_date = pytz.timezone('UTC').localize(due_date)
        except ValueError as e:
            return Response({"error": "잘못된 날짜 형식입니다."}, status=HTTP_400_BAD_REQUEST)

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
