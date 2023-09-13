from django.urls import path
from . import views  # board 앱의 views.py를 import

urlpatterns = [
    # 여기에 board 앱의 URL 패턴을 추가합니다.

    # list view
    path('suggestion', views.ListViewForSuggestion.as_view()),
    path('faq-board', views.ListViewForFaqBoard.as_view()),

    # comment list view
    path('suggestion/<int:suggestionId>/comment',
         views.ListViewForCommentForSuggestionForBoard.as_view()),

    # create view
    path('suggestion/add', views.CreateViewForSuggestionForBoard.as_view()),
    # board/suggestion/${suggestionId}/comment/create
    path('suggestion/<int:suggestionId>/comment/create',
         views.CreateViewForCommentForSuggestionForBoard.as_view()),

    # update view
    path('suggestion/<int:suggestionPk>/update',
         views.UpdateViewForSuggestionForBoard.as_view()),

    # delete view
    path('suggestion/<int:suggestionPk>/delete',
         views.DeleteViewForSuggestionForBoard.as_view()),

    path('suggestion/comment/<int:commentPk>/delete',
         views.DeleteViewForCommentForSuggestionForBoard.as_view()),

    # update view
    path('suggestion/comment/<int:commentPk>/update',
         views.UpdateViewForFaqComment.as_view()),

]
