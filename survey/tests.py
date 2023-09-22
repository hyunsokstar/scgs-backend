from django.test import TestCase

# Create your tests here.

# class ListViewForSurvey(APIView):
#     # pagination 관련 변수 선언
#     listForSurvey = []
#     perPage = 10
#     totalCountForSurveyList = 0

#     def get(self, request):
#         # pageNum 받아와서 초기화
#         pageNum = request.query_params.get("pageNum", 1)
#         pageNum = int(pageNum)

#         # Survey list data 가져 오기
#         list_for_survey = Survey.objects.all().order_by('-id')
#         self.listForSurvey = list_for_survey

#         # 총 개수 초기화
#         self.totalCountForSurveyList = list_for_survey.count()

#         # 범위 지정 하기
#         start = (pageNum - 1) * self.perPage
#         end = start + self.perPage
#         self.listForSurvey = self.listForSurvey[start:end]

#         # 해당 범위에 대해 listForSurveyList 직렬화
#         serializer = SurveySerializer(self.listForSurvey, many=True)

#         # 응답용 딕셔너리 선언
#         response_data = {
#             "listForSurvey": serializer.data,
#             "totalCountForSurveyList": self.totalCountForSurveyList,
#             "perPage": self.perPage,
#         }

#         # Response 로 응답용 딕셔너리 와 Http code 전달
#         return Response(response_data, status=HTTP_200_OK)