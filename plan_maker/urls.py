from django.urls import path
from . import views

# plan-maker

urlpatterns = [
    path('', views.LongTermPlanListAPIView.as_view(), name='long_term_plans'),
    path('<int:pk>', views.LongTermPlanDetailView.as_view(), name='long_term_plans'),
]
