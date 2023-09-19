from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForSurvey.as_view()),
    # path('test', views.TestViewForSurvey.as_view()),
]