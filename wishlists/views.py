from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound   
    
    # def get(self, request, pk):
    #     pass    

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},            
        )
        return Response(serializer.data)

    # def delete(self, request, pk):
    #     pass
    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)        

    # def put(self, request, pk):
    #     pass
    
    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(
                wishlist,
                context={"request": request},                
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    