from django.urls import path
from . import views
from .views import Tutorials


urlpatterns = [
    path('', views.Tutorials.as_view(), name='tutorials'),
    path("<int:pk>", views.TutorialDetail.as_view()),
    path("<int:pk>/like", views.TutorialLike.as_view()),
    path("<int:pk>/unlike", views.TutorialUnLike.as_view()),
]