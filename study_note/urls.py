from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyNoteAPIView.as_view(), name='StudyNoteAPIView'),
    path('contents/<int:content_pk>', views.StudyNoteContentView.as_view()),
    path('<int:study_note_pk>/contents', views.StudyNoteContentsView.as_view()), # 특정 노트의 contents 에 대한 crud
    path('<int:study_note_pk>/contents/delete-page', views.DeleteNoteContentsForSelectedPage.as_view()), # 특정 노트의 페이지에 대해 delete
    path('<int:pk>', views.StudyNoteDetailView.as_view(), name='api_docu_detail'),
    path('<int:study_note_pk>/contents/minus-one-page-for-selected-page', views.MinusOnePageForSelectedPageForStudyNoteContents.as_view()),
    path('<int:study_note_pk>/contents/plus-one-page-for-selected-page', views.PlusOnePageForSelectedPageForStudyNoteContents.as_view()),
    path('create-dummy', views.AddDummyDataForStudyNote.as_view(), name='AddDummyDataForStudyNote'),
    path('create-dummy-content', views.StudyNoteContentDummyAPI.as_view(), name='AddDummyDataForStudyNote')
]
