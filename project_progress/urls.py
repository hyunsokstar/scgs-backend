from django.urls import path
from . import views
from .views import ProjectProgressView

urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
]