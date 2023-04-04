from django.urls import path
from . import views

# tech_note/+@
urlpatterns = [
    path('insert-dummy-data', views.create_dummy_tech_notes,
         name='create_dummy_tech_notes'),
    path('', views.TechNotes.as_view(), name='tech-note-list'),
    # technote content view by pk <=> pk 는 technote의 pk 를 참조
    path('tech-note-content/<int:fk>', views.TechNoteContentsView.as_view(), name="tech-note-contents"),
    path('tech-note-content/<int:pk>/delete', views.TechNoteContentDeleteView.as_view(), name="tech-note-content-delete-view"),
    path('<int:pk>/view-count/update', views.UpdateViewForTechNoteViewCount.as_view(), name="update-view-for-tech-note-view-count"),

    path('<int:pk>/delete', views.TechNoteListDeleteView.as_view(),
         name='tech-note-list-delete'),
    path('<int:pk>/like', views.UpdateLikeView.as_view(),
         name='tech-note-list-delete'),
]
