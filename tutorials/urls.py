from django.urls import path
from . import views
from .views import Tutorials


urlpatterns = [
    path('', views.Tutorials.as_view(), name='tutorials'),
]