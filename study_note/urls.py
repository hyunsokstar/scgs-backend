from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyNoteAPIView.as_view(), name='StudyNoteAPIView'),
    path('<int:pk>', views.StudyNoteDetailView.as_view(), name='api_docu_detail'),
    path('create-dummy', views.AddDummyDataForStudyNote.as_view(), name='AddDummyDataForStudyNote'),
    path('create-dummy-content', views.StudyNoteContentDummyAPI.as_view(), name='AddDummyDataForStudyNote')
]
