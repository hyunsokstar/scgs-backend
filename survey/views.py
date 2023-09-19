from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Survey
from .serializers import SurveySerializer


class ListViewForSurvey(APIView):
    def get(self, request):
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TestViewForSurvey(APIView):
#     def get(self, request):

#         print("check for survey view test")

#         # 응답 데이터
#         data = {"message": "hello survey test!"}

#         # JsonResponse를 사용하여 JSON 형식의 응답을 반환
#         return JsonResponse(data, status=status.HTTP_200_OK)
