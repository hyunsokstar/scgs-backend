from django.urls import path
from . import views  # board 앱의 views.py를 import

urlpatterns = [
    # 여기에 board 앱의 URL 패턴을 추가합니다.
    path('suggestion', views.ListViewForSuggestion.as_view()),
    path('suggestion/add', views.CreateViewForSuggestionForBoard.as_view()),
]
