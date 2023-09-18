from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForChallenge.as_view()),
    path('<int:challengeId>/update/main_image', views.UpdateViewForChallengeMainImage.as_view()),
    path('create', views.CreateViewForChallenge.as_view()),

    # register view
    path('<int:challengeId>/register', views.ReigsterViewForChallenge.as_view()),

    # save view (create or update)
    path('<int:challengeId>/evaluation-criteria/save', views.SaveViewForEvaluationCriteriaForChallenge.as_view()),

    # detail view
    # 작업중
    path('<int:challengeId>/detail', views.DetailViewForChallenge.as_view()),

    # delete view
    # 삭제
    path('<int:challengeId>/withdrawl',
         views.WithDrawlViewForChallenge.as_view()),   
]
