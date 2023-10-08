from medias.models import PhotoForProfile
from medias.serializers import ProfilePhotoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddMultiUserSerializer, PrivateUserSerializer, SerializerForCreateForUserTaskComment, SerializerForManagerListForRegisterExtraManager, TaskStatusForTeamMembersSerializer, UserListSerializer, UserProfileImageSerializer, UserProfileSerializer, UsersForCreateSerializer
from users.models import User, UserPosition, UserTaskComment
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


# 임포트 관련
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated, ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from project_progress.models import ProjectProgress
from project_progress.serializers import ProjectProgressListSerializer
from datetime import datetime, time, timedelta
import math
import json


class ListViewForManagerListForRegisterExtraManager(APIView):
    def get(self, request, ownerUser):
        # 여기서 데이터를 가져오거나 처리합니다. 예: 데이터베이스 쿼리 등
        print("ownerUser : ", ownerUser)

        # extra_managers를 Query Parameter로부터 받아옵니다.
        extra_managers_str = request.GET.get('extra_managers', '[]')  # 기본값은 빈 JSON 배열 문자열
        extra_managers = json.loads(extra_managers_str)

        # 여기서 extra_managers 배열을 사용할 수 있습니다.
        print("extra_managers:::::::::::::: ??????? ", extra_managers)

        # 'task_manager' 내부의 'username' 값을 추출하여 배열로 만듦
        usernames = [item['task_manager']['username'] for item in extra_managers]

        # usernames 배열 출력
        print(usernames)

        # username 이 usernames 배열에 속하는거 제외 하고 가져 오려면?
        # managers = User.objects.exclude(username=ownerUser)
        managers = User.objects.exclude(username=ownerUser).exclude(username__in=usernames)

        serializer = SerializerForManagerListForRegisterExtraManager(
            managers, many=True)

        try:
            # 예시 데이터 (수정 필요)
            data = {
                "message": "데이터를 성공적으로 가져왔습니다.",
                "manager_list": serializer.data,
                # 기타 데이터 필드 추가
            }

            # 응답을 생성하고 반환합니다.
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            # 에러가 발생한 경우 에러 응답을 반환합니다.
            error_data = {
                "message": "데이터를 가져오는 중에 오류가 발생했습니다.",
                "error": str(e),  # 실제 에러 메시지 포함 가능
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteViewForUserCommentTaskByPk(APIView):
    def get_object(self, pk):
        try:
            return UserTaskComment.objects.get(pk=pk)
        except UserTaskComment.DoesNotExist:
            raise NotFound

    def delete(self, request, commentPk):
        comment_obj = self.get_object(commentPk)
        comment_obj.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class CreateViewForUserTaskComment(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, userPk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = SerializerForCreateForUserTaskComment(data=request.data)

        if serializer.is_valid():
            print("serializer 유효함")
            try:
                owner = self.get_object(userPk)
                test_for_task = serializer.save(writer=request.user)
                serializer = SerializerForCreateForUserTaskComment(
                    test_for_task)

                return Response({'success': 'true', "result": serializer.data}, status=HTTP_200_OK)

            except Exception as e:
                print("e : ", e)
                raise ParseError(
                    "error is occured for serailizer for create extra task")


class UncompletedTaskDataForSelectedUser(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []
    user_for_search = ""

    # get 요청에 대해
    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option (기간에 대해 검색)
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        user = User.objects.get(id=pk)

        # task_status_for_search
        task_status_option = request.query_params.get(
            "task_status_for_search", "")
        print("task_status_option : ", task_status_option)
        due_date_option_for_filtering = request.query_params.get(
            "due_date_option_for_filtering", "")
        print("due_date_option_for_filtering : ",
              due_date_option_for_filtering)

        self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
            task_completed=False, task_manager=user).order_by('-in_progress', '-created_at')

        print("self.all_uncompleted_project_task_list : ",
              self.all_uncompleted_project_task_list)

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

        user_info = TaskStatusForTeamMembersSerializer(user).data

        # step5 응답
        data = serializer.data
        data = {
            "user_info": user_info,
            "ProjectProgressList": data,
            "task_number_for_one_page": self.task_number_for_one_page,
            "totalPageCount": self.totalCountForTask,
            "count_for_ready": count_for_ready,
            "task_number_for_one_page": self.task_number_for_one_page,
            "count_for_in_progress": count_for_in_progress,
            "count_for_in_testing": count_for_in_testing,
        }

        return Response(data, status=HTTP_200_OK)


class CompletedTaskDataForSelectedUser(APIView):
    totalCountForTask = 0  # total_count 계산
    task_number_for_one_page = 50  # 1 페이지에 몇개씩
    all_uncompleted_project_task_list = []
    user_for_search = ""

    # get 요청에 대해
    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # period option (기간에 대해 검색)
        period_option = request.query_params.get(
            "selectedPeriodOptionForUncompletedTaskList", "all")

        user = User.objects.get(id=pk)

        # task_status_for_search
        task_status_option = request.query_params.get(
            "task_status_for_search", "")
        print("task_status_option : ", task_status_option)
        due_date_option_for_filtering = request.query_params.get(
            "due_date_option_for_filtering", "")
        print("due_date_option_for_filtering : ",
              due_date_option_for_filtering)

        self.all_uncompleted_project_task_list = ProjectProgress.objects.filter(
            task_completed=True, task_manager=user).order_by('-in_progress', '-created_at')

        print("self.all_uncompleted_project_task_list : ",
              self.all_uncompleted_project_task_list)

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

        # user_info = TaskStatusForTeamMembersSerializer(user).data

        # step5 응답
        data = serializer.data
        data = {
            # "user_info": user_info,
            "ProjectProgressList": data,
            "task_number_for_one_page": self.task_number_for_one_page,
            "totalPageCount": self.totalCountForTask,
        }

        return Response(data, status=HTTP_200_OK)


class MembersTaskStatus(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = TaskStatusForTeamMembersSerializer(users, many=True)
        data = serializer.data
        data.sort(key=lambda x: x['total_count_for_task'], reverse=True)
        return Response(data)


# Create your views here.
class UpdateViewForEditModeForStudyNoteContent(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def put(self, request, userPk):
        message = ""
        print("put 요청 확인 : pk ", userPk)
        user = self.get_object(userPk)

        if user.is_edit_mode_for_study_note_contents:
            message = "update for is_edit_mode_for_study_note_contents to off!"
            user.is_edit_mode_for_study_note_contents = False
        else:
            message = "test_passed to success!"
            user.is_edit_mode_for_study_note_contents = True

        user.save()

        result_data = {
            "success": True,
            "message": message,
        }

        return Response(result_data, status=status.HTTP_200_OK)


class UserNameListView (APIView):
    def get(self, request):
        users = User.objects.all()
        print("users : ", users)
        serializer = UsersForCreateSerializer(
            users, context={"request": request}, many=True)
        print("usernames only !! ", serializer.data)
        return Response(serializer.data)


class UserNameListViewWithOutMe (APIView):
    def get(self, request):
        users = User.objects.filter(~Q(username=request.user.username))
        print("users : ", users)
        serializer = UsersForCreateSerializer(
            users, context={"request": request}, many=True)
        print("usernames only !! ", serializer.data)
        return Response(serializer.data)


class DeleteMultiUsersView(APIView):
    def delete(self, request, format=None):
        user_ids = request.data.get('user_ids', None)
        if user_ids is not None:
            users = User.objects.filter(id__in=user_ids)
            users.delete()
            return Response({'message': 'Users deleted successfully'})
        else:
            return Response({'message': 'No user ids provided'})


# AddMultiRowsView(APIView) <=> 여러개의 행을 추가 with restapi using 배열 데이터 from client
class AddMultiUsersView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, format=None):
        users_data = request.data
        print("multi user 추가 요청 확인 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("users_data : ", users_data)

        for row in users_data:
            row_for_pk_exists = User.objects.filter(pk=row["pk"]).exists()
            print("row_for_pk_exists ::::::::::::::::::::::::::::::::: ",
                  row_for_pk_exists)
            print("row ::::: ", row)

            if (row_for_pk_exists == True):
                print("유저 테이블에 해당 정보가 존재 !")
                user = User.objects.get(pk=row["pk"])
                print("user :: ", user)

                if (user.username != row["username"]):
                    is_user_name_exits = User.objects.filter(
                        username=row["username"]).exists()
                    if is_user_name_exits:
                        print("is_user_name_exits : ", User.objects.get(
                            username=row["username"]))
                        raise ParseError("유저 이름이 이미 존재")
                    else:
                        user.username = row["username"]

                if row["position"] == "frontend" or row["position"] == "backend":
                    print("row position ", row["position"])
                    user_position = UserPosition.objects.get(
                        position_name=row["position"])
                    user.position = user_position
                else:
                    print("user position update by ", row["position"])
                    user_position = UserPosition.objects.get(
                        pk=row["position"])
                    user.position = user_position

                print("업데이트 하겠습니다 admin_level : ", row["admin_level"])
                user.name = row["name"]
                user.email = row["email"]
                user.admin_level = row["admin_level"]
                print("save 합니다 !!!!!!!!!!!!!!!!!!!")
                user.save()

            else:
                print("행 추가 ::", row)
                try:
                    serializer = AddMultiUserSerializer(
                        data=row)
                    if serializer.is_valid(raise_exception=True):
                        user = serializer.save()
                        user.set_password('1234')
                        user.save()
                except ValidationError as e:
                    return Response({'error': e.detail}, status=400)

        return Response({'message': 'Users saved successfully.'})


class UserProfile(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        print("디테일 페이지 요청 확인 (백엔드) !")
        print(pk, type(pk))
        user = self.get_object(pk)
        # print("user : ", user)
        serializer = UserProfileSerializer(
            user, context={"request": request})
        print("/users/:pk 에 대해 클라이언트로 넘너가는 데이터 serializer.data: ", serializer.data)
        return Response(serializer.data)

# 유저 이미지 업데이트

# UpdateViewForChallengeMainImage


class UserPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        user = self.get_object(pk)  # 개별 유저 가져 오기

        if request.user != user:
            raise PermissionDenied  # 현재 로그인한 사람이 아닐 경우 접근 거부

        serializer = UserProfileImageSerializer(
            user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def get(self, request):
        try:
            # user = User.objects.all()
            user = User.objects.all().order_by('-date_joined')
            # print("user : ", user)
            print("user count : ", len(user))
        except User.DoesNotExist:
            raise NotFound

        serializer = UserListSerializer(user, many=True)
        # print("userlist serializer result : ", serializer)

        if serializer:
            return Response(serializer.data)
        else:
            raise ParseError("serializer for api/v1/users is not valid")

    def post(self, request):
        password = request.data.get("password")
        username = request.data.get("username")
        email = request.data.get("email")

        userExists = User.objects.filter(username=username).exists()
        emailExists = User.objects.filter(email=email).exists()

        if (userExists):
            raise ParseError("유저 네임이 이미 존재")

        if (emailExists):
            raise ParseError("이메일이 이미 존재")

        if not password:
            raise ParseError("Password is missing")
        if not username:
            raise ParseError("username is missing")

        serializer = PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            new_user = authenticate(
                request, username=username, password=password)

            serializer = PrivateUserSerializer(user)
            if new_user is not None:
                login(request, new_user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Unable to log in with provided credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)

# /users/@{username}


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


# /users/change-password
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("username 이나 password 가 없습니다")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!", "user_name": user.username, "admin_level": user.admin_level})
        else:
            print("로그인 정보 틀렸음")
            raise ParseError("authentication info is wrong")


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"logout_success": True})

# class JWTLogIn(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         if not username or not password:
#             raise ParseError
#         user = authenticate(
#             request,
#             username=username,
#             password=password,
#         )
#         if user:
#             token = jwt.encode(
#                 {"pk": user.pk},
#                 settings.SECRET_KEY,
#                 algorithm="HS256",
#             )
#             return Response({"token": token})
#         else:
#             return Response({"error": "wrong password"})
