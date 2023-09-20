from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForSurvey.as_view()),
    path('createDataForTest', views.CreateDataForTest.as_view()),

    # create view
    path('<int:surveyId>/survey-option/create',
         views.CreateViewForSurveyOptionForSurvey.as_view()),
    # detail view
    path('<int:surveyId>', views.DetailViewForSurvey.as_view()),
]
