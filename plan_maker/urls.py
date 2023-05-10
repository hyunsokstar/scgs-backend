from django.urls import path
from . import views

# plan-maker

urlpatterns = [
    path('', views.LongTermPlanListAPIView.as_view(), name='long_term_plans'),
    path('contents/delete-for-checked', views.DeletePlanContentsForChecked.as_view()), 
    path('<int:pk>', views.LongTermPlanDetailView.as_view(), name='long_term_plans'),
    path('<int:pk>/contents/', views.LongTermPlanContentsView.as_view(), name='long_term_contents'),
    path('update-plan-contents-for-checked', views.LongTermPlanContentsUpdateView.as_view(), name='plan_contents_update_for_chekced')

]
