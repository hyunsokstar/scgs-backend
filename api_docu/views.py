from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApiDocuSerializer, SerializerForInsertToApiDocu
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, NotAuthenticated
from .models import ApiDocu
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

# test:
# http://127.0.0.1:8000/api/v1/api-docu/?page=1


class ApiDocuView(APIView):
    # step3 한 페이지당 목록 개수(per_page), 목록 총 개수(totalCount) 정의 하기
    toalCountForApiDocu = 0
    per_page = 5  

    # step4 목록 가져오는 함수 정의
    def get_api_docu_list(self):
        try:
            return ApiDocu.objects.all()
        except ApiDocu.DoesNotExist:
            raise NotFound

    def get(self, request):
        # step1 page 번호 받아 오기
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        # step2 페이지 번호 확인
        print("page : ", page)

        # step5 total count
        self.toalCountForApiDocu = self.get_api_docu_list().count()

        # step6 총 개수
        print("총개수 check (self.toalCountForApiDocu) : ", self.toalCountForApiDocu)

        # step7 해당 페이지의 ApiDocu목록 가져 오기
        # step7-1 범위 정하기 (start ~ end)
        start = (page - 1) * self.per_page
        end = start + self.per_page
        # step 7-2 해당 범위의 목록 가져 오기
        list_for_api_docu_for_page = self.get_api_docu_list()[start:end]        

        # step 8 시리얼라이저로 직렬화 
        serializer = ApiDocuSerializer(list_for_api_docu_for_page, many=True)

        data = {
            "totalCount": self.toalCountForApiDocu,
            "api_docu_list": serializer.data
        }
        return Response(data, status=HTTP_200_OK)
        # return Response(response_data, status=status.HTTP_200_OK)

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
