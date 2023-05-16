from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("", views.Users.as_view()),
    path("members-task-status", views.MembersTaskStatus.as_view()),
    path("me", views.Me.as_view()),
    path("only-user-name", views.UserNameListView.as_view()),
    path("multi-users", views.AddMultiUsersView.as_view()),
    path("multi-users/delete", views.DeleteMultiUsersView.as_view()),
    path("<int:pk>", views.UserProfile.as_view()),
    path("<int:userPk>/comment", views.CreateViewForUserTaskComment.as_view()),
    path("comment/<int:commentPk>/delete", views.DeleteViewForUserCommentTaskByPk.as_view()),

    path("<int:pk>/comment", views.UserProfile.as_view()),
    path("<int:pk>/task-data-for-uncompleted", views.UncompletedTaskDataForSelectedUser.as_view()),

    path("<int:userPk>/EditModeForStudyNoteForContent/update",
         views.UpdateViewForEditModeForStudyNoteContent.as_view()),
    path("<int:pk>/photos", views.UserPhotos.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("token-login", obtain_auth_token),
    path("@<str:username>", views.PublicUser.as_view()),
]
