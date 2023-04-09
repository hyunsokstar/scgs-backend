from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApiDocuSerializer, SerializerForInsertToApiDocu
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from .models import ApiDocu
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK



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


class ApiDocuDetailView(APIView):
    def get_object(self, pk):
        try:
            return ApiDocu.objects.get(pk=pk)
        except ApiDocu.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        api_docu = self.get_object(pk)
        api_docu.delete()

        return Response(status=HTTP_204_NO_CONTENT)
