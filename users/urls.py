from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("me", views.Me.as_view()),
    path("", views.Users.as_view()),
    path("<int:pk>", views.UserProfile.as_view()),
    path("<int:pk>/photos", views.UserPhotos.as_view()),    
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),    
    path("change-password", views.ChangePassword.as_view()),
    path("token-login", obtain_auth_token),
    # path("jwt-login", views.JWTLogIn.as_view()),    
    path("@<str:username>", views.PublicUser.as_view()) 
]