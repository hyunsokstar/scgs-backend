from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortCut
from .serializers import ShortCutSerializer


class ShortCutListView(APIView):
    def get(self, request):
        shortcuts = ShortCut.objects.all()
        serializer = ShortCutSerializer(shortcuts, many=True)
        response_data = {
            'success': True,
            'shortcut_list': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)