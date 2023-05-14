from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShortCutListView.as_view()),
    path('<int:pk>', views.ShortCutDetailView.as_view()),
    path('related-shortcut/<int:pk>', views.DeketeRekatedShortCutView.as_view()),
    path('related-shortcut/delete-for-chekced-row',
         views.DeleteRelatedShortcutForCheckedRow.as_view()),
]
