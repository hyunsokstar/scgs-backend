from django.urls import path
from . import views
from .views import Estimates, EstimateDetail

urlpatterns = [
    path('', views.Estimates.as_view(), name='estimates'),
    path("<int:pk>", views.EstimateDetail.as_view()),
]