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
    path('faq-board/<int:faqId>/comment',
         views.ListViewForCommentForFaqForBoard.as_view()),     
         
     

    # create view
    path('suggestion/add', views.CreateViewForSuggestionForBoard.as_view()),
    path('faq-bard/create', views.CreateViewForFaqForBoard.as_view()),
    path('suggestion/<int:suggestionId>/comment/create',
         views.CreateViewForCommentForSuggestionForBoard.as_view()),
     # board/faq/${faqId}/comment/create
    path('faq-board/<int:faqId>/comment/create',
         views.CreateViewForCommentForFaqForBoard.as_view()),

    # update view
    path('suggestion/<int:suggestionPk>/update',
         views.UpdateViewForSuggestionForBoard.as_view()),

    path('faq-board/comment/<int:commentId>/update',
         views.UpdateViewForCommentForFaqForBoard.as_view()), 

    path('suggestion/comment/<int:commentPk>/update',
         views.UpdateViewForFaqComment.as_view()),

    # delete view
    path('faq-board/<int:faqId>/delete',
         views.DeleteViewForFaqForBoard.as_view()),

    path('suggestion/<int:suggestionPk>/delete',
         views.DeleteViewForSuggestionForBoard.as_view()),

    path('suggestion/comment/<int:commentPk>/delete',
         views.DeleteViewForCommentForSuggestionForBoard.as_view()),

    path('faq-board/comment/<int:commentPk>/delete',
         views.DeleteViewForCommentForFaqForBoard.as_view()),


]
