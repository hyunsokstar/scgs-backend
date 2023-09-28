from django.urls import path
from . import views

urlpatterns = [
    #     list view
    path('', views.ListViewForChallenge.as_view()),
    path('<int:challengeId>/challenge-ref/list',
         views.ListViewForChallengeRef.as_view()),
    path('<int:challengeId>/challenger-ref/list',
         views.ListViewForChallengerRef.as_view()),

    # create view
    path('create', views.CreateViewForChallenge.as_view()),
    # ${challengeId}/challenge-comment/create
    path('<int:challengeId>/challenge-comment/create',
         views.CreateViewForCommentForChallenge.as_view()),
    # ${challengeId}/challenge-ref/create
    path('<int:challengeId>/challenge-ref/create',
         views.CreateViewForChallengeRef.as_view()),
    path('<int:challengeId>/challenger-ref/create',
         views.CreateViewForChallengerRef.as_view()),

    # register view
    path('<int:challengeId>/register', views.ReigsterViewForChallenge.as_view()),

    # save view (create or update)
    path('<int:challengeId>/evaluation-criteria/save',
         views.SaveViewForEvaluationCriteriaForChallenge.as_view()),

    # detail view
    path('<int:challengeId>/detail', views.DetailViewForChallenge.as_view()),

    # delete view
    path('<int:challengeId>/withdrawl',
         views.WithDrawlViewForChallenge.as_view()),
    # challenge-comment/${commentId}/delete
    path('challenge-comment/<int:commentId>/delete',
         views.DeleteViewForCommentForChallenge.as_view()),

    path('<int:challengeId>/delete',
         views.DeleteViewForChallenge.as_view()),

    path('challenge-ref/<int:challengeRefId>/delete',
         views.DeleteViewForChallengeRef.as_view()),
    path('challenger-ref/<int:challengerRefId>/delete',
         views.DeleteViewForChallengerRef.as_view()),

    # update view
    path('<int:challengeId>/update/evaluate-result',
         views.UpdateViewForEvaluateResultForChallenge.as_view()),
    path('<int:challengeId>/update',
         views.UpdateViewForChallenge.as_view()),
    path('<int:challengeId>/update/main_image',
         views.UpdateViewForChallengeMainImage.as_view()),
    #  `/challenge-ref/${challengeRefId}/update`,
    path('challenge-ref/<int:challengeRefId>/update',
         views.UpdateViewForChallengeRef.as_view()),
    path('challenger-ref/<int:challengerRefId>/update',
         views.UpdateViewForChallengerRef.as_view()),

    # challenge resut meta info update
    path('challenge-result/<int:challengeResultId>/update',
         views.UpdateViewForChallengeResultMetaInfo.as_view()),

    # ${challengeResultId}/passed/update
    path('<int:challengeResultId>/passed/update',
         views.UpdateViewForChallengeResultPassed.as_view()),
]
