from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListViewForChallenge.as_view()),
    path('<int:challengeId>/update/main_image',
         views.UpdateViewForChallengeMainImage.as_view()),

    # create view
    path('create', views.CreateViewForChallenge.as_view()),
    # ${challengeId}/challenge-comment/create
    path('<int:challengeId>/challenge-comment/create',
         views.CreateViewForCommentForChallenge.as_view()),

    # register view
    path('<int:challengeId>/register', views.ReigsterViewForChallenge.as_view()),

    # save view (create or update)
    path('<int:challengeId>/evaluation-criteria/save',
         views.SaveViewForEvaluationCriteriaForChallenge.as_view()),

    # detail view
    # 작업중
    path('<int:challengeId>/detail', views.DetailViewForChallenge.as_view()),

    # delete view
    # 삭제
    path('<int:challengeId>/withdrawl',
         views.WithDrawlViewForChallenge.as_view()),

     # challenge-comment/${commentId}/delete
    path('challenge-comment/<int:commentId>/delete',
         views.DeleteViewForCommentForChallenge.as_view()),

    path('<int:challengeId>/delete',
         views.DeleteViewForChallenge.as_view()),

    # update view
    path('<int:challengeId>/update/evaluate-result',
         views.UpdateViewForEvaluateResultForChallenge.as_view()),
    path('<int:challengeId>/update',
         views.UpdateViewForChallenge.as_view()),

    # challenge resut meta info update
    path('challenge-result/<int:challengeResultId>/update',
         views.UpdateViewForChallengeResultMetaInfo.as_view()),


    # ${challengeResultId}/passed/update
    path('<int:challengeResultId>/passed/update',
         views.UpdateViewForChallengeResultPassed.as_view())

]
