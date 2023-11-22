from django.urls import path
from . import views
from .views import Estimates, EstimateDetail

urlpatterns = [
    path('', views.Estimates.as_view(), name='estimates'),
    path('delete', views.DeleteEstimatesForCheck.as_view(), name="delete_estimate_for_pk"),
    path("<int:pk>", views.EstimateDetail.as_view()),
]