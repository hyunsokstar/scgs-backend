from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApiDocuSerializer

from .models import ApiDocu

class ApiDocuView(APIView):
    def get(self, request):
        apis = ApiDocu.objects.all()
        serializer = ApiDocuSerializer(apis, many=True)
        response_data = {
            'success': True,
            'api_docu_list': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
