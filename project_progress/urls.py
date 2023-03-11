from django.urls import path
from . import views
from .views import ProjectProgressView, UpdateTaskCompetedView

urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
    path("<int:pk>/completed/update", views.UpdateTaskCompetedView.as_view()),
]