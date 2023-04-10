from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from .models import ShortCut
from .serializers import SerializerForInsertToShortcut, ShortCutSerializer

class ShortCutListView(APIView):
    def get(self, request):
        print("shortcut list 요청 받음")
        shortcuts = ShortCut.objects.all()
        serializer = ShortCutSerializer(shortcuts, many=True)
        response_data = {
            'success': True,
            'shortcut_list': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # print("request.data['shortcut] : ", request.data['shortcut'])
        # print("request.data['description] : ", request.data['description'])
        # print("request.data['classification] : ",
        #       request.data['classification'])

        serializer = SerializerForInsertToShortcut(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                shortcut = serializer.save(writer=request.user)
            else:
                shortcut = serializer.save()

            serializer = ShortCutSerializer(shortcut)
        else:
            print("serializer.errors : ", serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)

        return Response({"success": True, "data": serializer.data})

# ShortCutDetailView
class ShortCutDetailView(APIView):
    def get_object(self, pk):
        try:
            return ShortCut.objects.get(pk=pk)
        except ShortCut.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        shortcut = self.get_object(pk)
        shortcut.delete()

        return Response(status=HTTP_204_NO_CONTENT)