from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyNoteAPIView.as_view(), name='StudyNoteAPIView'),
    path('contents/<int:study_note_pk>', views.StudyNoteContentsView.as_view(), name='StudyNoteAPIView'),
    path('<int:pk>', views.StudyNoteDetailView.as_view(), name='api_docu_detail'),
    path('<int:study_note_pk>/contents/plun-one-page-for-selected-page', views.PlusOnePageForSelectedPageForStudyNoteContents.as_view(), name='api_docu_detail'),
    path('create-dummy', views.AddDummyDataForStudyNote.as_view(), name='AddDummyDataForStudyNote'),
    path('create-dummy-content', views.StudyNoteContentDummyAPI.as_view(), name='AddDummyDataForStudyNote')
]
