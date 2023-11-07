from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShortCutListView.as_view()),
    path('register-to-hub', views.ListViewForShortForRegisterToHub.as_view()),
    path('hub', views.ListViewForShortCutHub.as_view()),
    path('hub/<int:hub_id>/content', views.ListViewForShortCutHubContent.as_view()),
    path('hub/create', views.CreateViewForShortCutHub.as_view()),
    path('<int:pk>', views.ShortCutDetailView.as_view()),
    path('related-shortcut/<int:pk>', views.RelatedShortCutView.as_view()),
    path('related-shortcut/delete-for-checked-row',
         views.DeleteRelatedShortcutForCheckedRow.as_view()),
]
