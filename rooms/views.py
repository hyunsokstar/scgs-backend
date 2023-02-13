import time

from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT

from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from .models import Amenity, Room
from categories.models import Category

from django.db import transaction
from reviews.serializers import ReviewSerializer
from django.http import JsonResponse
from django.conf import settings

from medias.serializers import PhotoSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bookings.models import Booking

from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


from django.utils import timezone   

class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound    
    
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)    

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)



class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        print("room list 출력 확인")
        # time.sleep(2)
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request": request})        
        return Response(serializer.data)
    
    def post(self, request):
        
        print("룸 포스팅 test 확인 !!")
        
        serializer = RoomDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            # 카테고리 정보 초기화 
            category_pk = request.data.get("category")
            if not category_pk:
                print("카테고리가 없습니다")
                # raise ParseError
                raise ParseError("Category is required.")                    
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category's kind should be 'rooms'")                        
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            
            try:
                with transaction.atomic():               
                    room = serializer.save(
                        owner=request.user, 
                        category=category                
                    )
                    amenities = request.data.get("amenities")
                    print("amenities : ", amenities)
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        print("amenity : ", amenity)
                        room.amenities.add(amenity)   
                        
                    print("room : ", room)        
                    serializer = RoomDetailSerializer(room,context={"request": request})
                    return Response(serializer.data)
            except Exception as e:
                print("여기에서 에러 발생 !!!!!!" , e)
                raise ParseError("Amenity not found")
                
        else:
            print("시리얼 라이저가 유효하지 않음")
            return Response(serializer.errors)           
    
class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]    
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # time.sleep(2)
        print("디테일 페이지 요청 확인 (백엔드) !")
        print(pk, type(pk))
        room = self.get_object(pk)
        print("room : ", room)
        serializer = RoomDetailSerializer(room, context={"request":request})             
        print("serializer.data: ", serializer.data)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT) 
    
    def put(self, request, pk):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            # 시리얼 라이저가 유효하다면 해당 룸에 대해 수정 작업을 시작해 보자 
            # 룸 정보 가져오기 by pk
            room = self.get_object(pk)        
            # 수정 권한 확인 <=> 룸의 오너가 맞는지 확인 하기 
            if room.owner != request.user:
                raise PermissionDenied        
            # 로그인 했는지확인        
            # if not request.user.is_authenticated:
                # raise NotAuthenticated        
            # 카테고리 정보 가져와서 카테고리 객체로 만들기
            try:
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                # 카테고리 객체             
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category's kind should be 'rooms'")                     
            except Category.DoesNotExist:
                raise ParseError("Category not found")         
        
            try:
                # 만약 요청 데이터중 amenties가 유효하지 않다면(없다면) 에러 처리 + 룸 save 에 대한 되돌리기 
                with transaction.atomic():               
                    # 일단 save 하는데 유저 정보와 카테고리 정보까지
                    room = serializer.save(
                            owner=request.user, 
                            category=category                
                        )
                # 기존 amenities 삭제
                room.amenities.clear()                
                amenities = request.data.get("amenities")
                print("amenities : ", amenities)
                
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    room.amenities.add(amenity)   
                
                # amenities 까지 업데이트 한후 응답    
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)                    
            except Exception:
                raise ParseError("Amenity not found")
        else:
            print("시리얼 라이저가 유효하지 않음")
            return Response(serializer.errors)
        
class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]    
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)

        except ValueError:
            page = 1

        # page_size = 3
        page_size = settings.PAGE_SIZE        
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True
        )

        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk)
            )
            
            serializer = ReviewSerializer(review)
            return Response(serializer.data)    
    

class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]    
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# rooms/{room id}/bookings
class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,            
        )
        
        print("bookings : ", bookings)
        
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room}
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

class RoomBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_in,
            check_out__gte=check_out,
        ).exists()

        if exists:
            return Response({"ok": False})
        return Response({"ok": True})
