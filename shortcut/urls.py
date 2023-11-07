from django.urls import path
from . import views

urlpatterns = [
    path('hub', views.ListViewForShortCutHub.as_view()),
    path('hub/create', views.CreateViewForShortCutHub.as_view()),
    path('', views.ShortCutListView.as_view()),
    path('<int:pk>', views.ShortCutDetailView.as_view()),
    path('related-shortcut/<int:pk>', views.RelatedShortCutView.as_view()),
    path('related-shortcut/delete-for-checked-row',
         views.DeleteRelatedShortcutForCheckedRow.as_view()),
]
