from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
    path("<int:pk>/completed/update", views.UpdateTaskCompetedView.as_view()),
    path("<int:pk>/importance/update",
         views.UpdateProjectTaskImportance.as_view()),
    path("<int:pk>", views.ProjectProgressDetailView.as_view()),
    
]
