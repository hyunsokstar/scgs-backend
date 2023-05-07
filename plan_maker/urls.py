from django.urls import path
from . import views

urlpatterns = [
    path('', views.LongTermPlanListAPIView.as_view(), name='long_term_plans'),
]
