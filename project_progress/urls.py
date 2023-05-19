from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectProgressView.as_view(), name='project_progress'),
    path('task-status-view-for-today', views.TaskStatusViewForToday.as_view()),
    path('DailyCompletedTasks', views.DailyCompletedTasks.as_view()),
    path('update-task-manager-for-checked',
         views.UpdateForTaskManagerForChecked.as_view()),
    path('update-task-importance-for-checked',
         views.UpdateForTaskImportanceForChecked.as_view()),
    path('update-task-clasification-for-checked',
         views.UpdateForTaskClassificationForChecked.as_view()),
    path('task-list-for-checked', views.taskListForChecked.as_view(),
         name='project_progress'),
    path('update-task-due-date-for-checked',
         views.UpdateViewForTaskDueDateForChecked.as_view()),

    path('delete-for-checked', views.DeleteTasksForChecked.as_view(),
         name='project_progress'),
    path("<int:pk>", views.ProjectProgressDetailView.as_view()),

    path('task-statics', views.TaskStaticsIView.as_view()),
    path('<int:userPk>/daily-task-count',
         views.TaskStaticsIViewForPersnalUser.as_view()),

    path('writer-info', views.TaskMangerInfo.as_view()),
    path('extra_tasks', views.ExtraTasks.as_view(), name='extra_tasks'),
    path('extra_tasks/<int:pk>', views.ExtraTasks.as_view(), name='extra_tasks'),
    path('task-status', views.TaskStatusListView.as_view(), name="task_status_view"),

    path("tasks-with-cash-prize", views.TasksWithCashPrize.as_view(),
         name="completed_task_list"),

    path("uncompleted", views.UncompletedTaskListView.as_view(),
         name="completed_task_list"),
    path("uncompleted/for-me", views.UncompletedTaskListViewForMe.as_view(),
         name="uncompleted_task_list_for_me"),
    path("completed", views.CompletedTaskListView.as_view(),
         name="completed_task_list"),
    path("completed/for-me", views.CompletedTaskListViewForMe.as_view(),
         name="completed_task_list_for_me"),

    path("<int:pk>/completed/update", views.UpdateTaskCompetedView.as_view()),
    path("<int:pk>/is_task_for_cash_prize/update",
         views.update_task_for_is_task_for_cash_prize.as_view()),
    path("<int:pk>/is_task_for_urgent/update",
         views.update_task_for_is_task_for_urgent.as_view()),
    path("<int:pk>/check-result/update",
         views.UpdateCheckResultByTesterView.as_view()),
    path("<int:pk>/check_for_cash_prize/update",
         views.UpdateCheckForCashPrize.as_view()),


    path("<int:pk>/score-by-tester/update",
         views.UpdateScoreByTesterView.as_view()),
    path("<int:pk>/in_progress/update", views.UpdateTaskInProgressView.as_view()),
    path("<int:pk>/is_testing/update", views.UpdateTaskIsTestingView.as_view()),
    path("<int:pk>/importance/update",
         views.UpdateProjectTaskImportance.as_view()),

    path("<int:pk>/importance/update",
         views.UpdateProjectTaskImportance.as_view()),

    path("<int:pk>/cash_prize/update",
         views.UpdateForCashPrizeForTask.as_view()),

    path("<int:pk>/update_project_status_page/update",
         views.UpdateProjectStatusPageView.as_view()),

    path("<int:pk>/due_date/update",
         views.UpdateProjectTaskDueDate.as_view()),
    path("<int:pk>/started_at/update",
         views.UpdateProjectTaskStartedAt.as_view()),
    path("<int:taskPk>/comment", views.ProjectProgressCommentView.as_view()),
    path("comment/<int:commentPk>/edit-mode/update",
         views.UpdateViewForCommentEdit.as_view()),
    path("comment/<int:commentPk>/comment/update",
         views.UpdateViewForCommentText.as_view()),
    path("comment/<int:commentPk>", views.CommentForTaskView.as_view()),

    path("<int:taskPk>/TestForTasks", views.TestForTasks.as_view()),
    path("TestForTasks/<int:testPk>/delete",
         views.DeleteTestForTasksView.as_view()),
    path("TestForTasks/<int:testPk>/update/testers",
         views.UpatedTestersForTestPkView.as_view()),
    path("<int:taskPk>/challengers-for-cash-prize/update",
         views.UpatedChallengersForCashPrize.as_view()),
    path("TestForTasks/<int:testPk>/update",
         views.UpatedTestPassedForTasksView.as_view())
]
