from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForChallenge.as_view()),

]
