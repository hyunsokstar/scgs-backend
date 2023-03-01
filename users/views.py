from medias.models import PhotoForProfile
from medias.serializers import ProfilePhotoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from users.models import User
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

# 임포트 관련
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.exceptions import ParseError, NotFound
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated


from django.conf import settings
import jwt


# Create your views here.
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
        serializer = serializers.UserProfileSerializer(user, context={"request":request})             
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
            if(exist_photo):
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
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class Users(APIView):
    def get(self, request):
        try:
            # user = User.objects.get(username=username)
            user = User.objects.all()
            print("first : ", user)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.UserListSerializer(user, many=True)
        return Response(serializer.data)    
    
    def post(self, request):
        
        password = request.data.get("password")
        username = request.data.get("username")
        
        if not password:
            raise ParseError("Password is missing")     
        if not username:
            raise ParseError("username is missing")             
        
        serializer = serializers.PrivateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            
            new_user = authenticate(request, username=username, password=password)

            serializer = serializers.PrivateUserSerializer(user)
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
        serializer = serializers.PrivateUserSerializer(user)
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
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"}) 
    
class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})