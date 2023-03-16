from medias.models import PhotoForProfile
from medias.serializers import ProfilePhotoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddMultiUserSerializer, PrivateUserSerializer, UserListSerializer, UserProfileSerializer
from users.models import User, UserPosition
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

# 임포트 관련
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.exceptions import ParseError, NotFound
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated, ValidationError


from django.conf import settings
import jwt


# Create your views here.

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
            print("row_for_pk_exists ::::::::::::::::::::::::::::::::: ", row_for_pk_exists)

            if (row_for_pk_exists ==True):
                print("실행 check here here here")
                user = User.objects.get(pk=row["pk"])
                print("user :: ", user)

                if (user):
                    print("업데이트 하겠습니다")
                    if (row["username"] != user.username):
                        is_user_name_exits = User.objects.filter(
                            username=row["username"]).exists()
                        user_position = UserPosition.objects.get(
                            pk=row["position"])

                        if (user_position == ""):
                            raise ParseError("유저 postion 을 선택 안하셨습니다")

                        if is_user_name_exits:
                            print("is_user_name_exits : ", User.objects.get(
                                username=row["username"]))
                            raise ParseError("유저 이름이 이미 존재")

                        user.name = row["name"]
                        user.username = row["username"]
                        user.email = row["email"]
                        user.admin_level = row["admin_level"]
                        user.position = user_position
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

        serializer = ProfilePhotoSerializer(data=request.data)

        if serializer.is_valid():

            exist_photo = PhotoForProfile.objects.filter(user=user)
            if (exist_photo):
                result = exist_photo.delete()
                print("result : ", result)

            photo = serializer.save(user=user)
            print("photo : ", photo)
            serializer = ProfilePhotoSerializer(photo)
            print("serializer : ", serializer.data)
            return Response(serializer.data)
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
            return Response({"ok": "Welcome!"})
        else:
            print("로그인 정보 틀렸음")
            raise ParseError("authentication info is wrong")


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})

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
