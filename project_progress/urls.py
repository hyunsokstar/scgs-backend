from django.urls import path
from . import views

# /project_progress/ + @
urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
    path("uncompleted", views.UncompletedTaskListView.as_view(), name ="completed_task_list"),
    path("uncompleted/for-me", views.UncompletedTaskListViewForMe.as_view(), name ="uncompleted_task_list_for_me"),
    path("completed", views.CompletedTaskListView.as_view(), name ="completed_task_list"),
    path("completed/for-me", views.CompletedTaskListViewForMe.as_view(), name ="completed_task_list_for_me"),
    path("<int:pk>/completed/update", views.UpdateTaskCompetedView.as_view()),
    path("<int:pk>/in_progress/update", views.UpdateTaskInProgressView.as_view()),
    path("<int:pk>/importance/update",
         views.UpdateProjectTaskImportance.as_view()),
    path("<int:pk>/due_date/update",
         views.UpdateProjectTaskDueDate.as_view()),
    path("<int:pk>/started_at/update",
         views.UpdateProjectTaskStartedAt.as_view()),
    path("<int:pk>", views.ProjectProgressDetailView.as_view()),

]
