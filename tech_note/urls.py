from django.urls import path
from . import views

urlpatterns = [
    path('insert-dummy-data', views.create_dummy_tech_notes,
         name='create_dummy_tech_notes'),
    path('', views.TechNotes.as_view(), name='tech-note-list'),
    # technote content view by pk <=> pk 는 technote의 pk 를 참조
    path('<int:pk>', views.TechNoteContentView.as_view(), name="tech-note-contents"),
    path('<int:pk>/delete', views.TechNoteListDeleteView.as_view(),
         name='tech-note-list-delete'),
    path('<int:pk>/like', views.UpdateLikeView.as_view(),
         name='tech-note-list-delete'),
]
