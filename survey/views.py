from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import Survey, SurveyOption, SurveyAnswer
from .serializers import SurveySerializer, SurveyDetailSerializer

# 1122


class CreateViewForSurveyOptionForSurvey(APIView):
    def post(self, request, surveyId):
        # surveyId를 기반으로 Survey를 가져옵니다.
        try:
            survey = Survey.objects.get(pk=surveyId)
        except Survey.DoesNotExist:
            return Response(
                {"message": "해당 Survey를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        # API에서 전달된 데이터에서 newOption을 추출합니다.
        newOption = request.data.get("newOption", "")

        # 작성자의 유저네임과 현재 유저의 유저네임을 비교합니다.
        if survey.writer.username != request.user.username:
            return Response(
                {"message": "옵션을 추가할 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # SurveyOption을 생성하고 저장합니다.
        survey_option = SurveyOption(survey=survey, content=newOption)
        survey_option.save()

        # 적절한 응답을 반환합니다.
        response_message = f"{survey.title}에 '{newOption}' 옵션을 추가했습니다."
        return Response(
            {"message": response_message},
            status=status.HTTP_201_CREATED
        )

# http://127.0.0.1:8000/api/v1/survey/1
class DetailViewForSurvey(APIView):
    def get(self, request, surveyId):
        try:
            survey = Survey.objects.get(id=surveyId)
            serializer = SurveyDetailSerializer(survey)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Survey.DoesNotExist:
            return Response(
                {"message": "Survey not found"},  # 수정된 부분
                status=status.HTTP_404_NOT_FOUND
            )


class CreateDataForTest(APIView):
    def get(self, request):
        # Survey 모델에 10개의 설문 추가
        for i in range(10):
            survey = Survey.objects.create(
                title=f"Survey {i}",
                description=f"This is survey {i}",
                # 작성자 필드가 null=True, blank=True 이므로 None으로 둘 수 있습니다.
                writer=None
            )
            # SurveyOption 모델에 몇 가지 옵션을 추가
            for j in range(3):  # 각 설문에 3개의 옵션을 추가합니다.
                SurveyOption.objects.create(
                    survey=survey,
                    content=f"Option {j} for survey {i}"
                )

            # SurveyAnswer 모델에 몇 가지 답변 추가
            user = User.objects.first()  # 적절한 사용자를 가져오거나 적절하게 설정하세요.
            for _ in range(2):  # 각 설문에 2개의 답변을 추가합니다.
                selected_option = survey.survey_options.all().order_by('id').first()
                SurveyAnswer.objects.create(
                    participant=user,
                    survey=survey,
                    selected_option=selected_option
                )

        return Response("Test data created successfully", status=status.HTTP_201_CREATED)


class ListViewForSurvey(APIView):
    def get(self, request):
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
