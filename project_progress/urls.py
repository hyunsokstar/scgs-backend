from django.urls import path
from . import views

# /project_progress/ + @
urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
    path("uncompleted", views.UncompletedTaskListView.as_view(), name ="completed_task_list"),
    path("completed", views.CompletedTaskListView.as_view(), name ="completed_task_list"),
    path("<int:pk>/completed/update", views.UpdateTaskCompetedView.as_view()),
    path("<int:pk>/importance/update",
         views.UpdateProjectTaskImportance.as_view()),
    path("<int:pk>", views.ProjectProgressDetailView.as_view()),

]
