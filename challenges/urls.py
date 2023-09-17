from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForChallenge.as_view()),
    path('<int:challengeId>/update/main_image', views.UpdateViewForChallengeMainImage.as_view()),
    path('create', views.CreateViewForChallenge.as_view()),
    # save view for grid table
    path('<int:challengeId>/evaluation-criteria/save', views.SaveViewForEvaluationCriteriaForChallenge.as_view()),

]
