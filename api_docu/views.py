from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApiDocuSerializer, SerializerForInsertToApiDocu
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated

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

    def post(self, request):
        print("request.data['url] : ", request.data['url'])
        print("request.data['description] : ", request.data['description'])
        print("request.data['classification] : ",
              request.data['classification'])

        serializer = SerializerForInsertToApiDocu(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                api_docu = serializer.save(writer=request.user)
            else:
                api_docu = serializer.save()

            serializer = SerializerForInsertToApiDocu(api_docu)
        else:
            print("serializer.errors : ", serializer.errors)
            error_message = serializer.errors
            raise ParseError(error_message)

        return Response({"success": True, "data": serializer.data})
