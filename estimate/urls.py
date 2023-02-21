from django.urls import path
from . import views
from .views import Estimates

urlpatterns = [
    path('', views.Estimates.as_view(), name='estimates'),
]