from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiDocuView.as_view(), name='project_progress'),
]
