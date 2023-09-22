from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForSurvey.as_view()),
    path('search', views.SearchViewForSurveyList.as_view()),
    path('createDataForTest', views.CreateDataForTest.as_view()),

    # create view
    path('create',
         views.CreateViewForSurvey.as_view()),

    path('<int:surveyId>/survey-option/create',
         views.CreateViewForSurveyOptionForSurvey.as_view()),

    path('survey-answer/create',
         views.CreateViewForSurveyAnswerForSurvey.as_view()),

    # detail view
    path('<int:surveyId>', views.DetailViewForSurvey.as_view()),

    # ${surveyId}/delete
    path('<int:surveyId>/delete', views.DeleteViewForSurvey.as_view()),


]
