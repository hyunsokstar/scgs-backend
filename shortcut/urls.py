from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShortCutListView.as_view()),
]
