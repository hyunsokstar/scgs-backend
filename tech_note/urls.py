from django.urls import path
from . import views

urlpatterns = [
    path('insert-dummy-data', views.create_dummy_tech_notes, name='create_dummy_tech_notes'),
    path('', views.TechNotes.as_view(), name='tech-note-list'),
    path('<int:pk>/delete', views.TechNoteListDeleteView.as_view(), name='tech-note-list-delete'),
]
