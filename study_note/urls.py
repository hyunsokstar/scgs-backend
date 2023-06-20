from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudyNoteAPIView.as_view(), name='StudyNoteAPIView'),
    path('<int:notePk>/', views.StudyNoteDetailView.as_view()),
    path('comment/<int:commentPk>/delete', views.DeleteViewForStudyNoteComment.as_view()),
    path('comment/<int:commentPk>/update-comment', views.UpdateViewForStudyNoteComment.as_view()),

    path('<int:studyNotePk>/create-comment', views.CreateViewForCommentForNote.as_view()),
    path('comment/<int:commentPk>/update-edit-mode', views.UpdateViewForEditModeForStudyNoteBriefingBoard.as_view(), name='StudyNoteAPIView'),
    path('update-is-approved-for-cowriter',
         views.UpdateViewForIsApprovedForCoWorker.as_view()),
    path('get-study-note-list-for-copy-mode',
         views.StudyNoteAPIViewForCopyMode.as_view(), name='StudyNoteAPIView'),
    path('get-study-note-for-checked-rows/',
         views.StudyNoteAPIViewForCheckedRows.as_view(), name='StudyNoteAPIView'),
    path('for-me/', views.StudyNoteAPIViewForMe.as_view()),
    path('<int:pk>/contents/update/re-order-for-contents',
         views.StudyNoteContentReOrderAPIView.as_view(), name='study-note-contents-re-order'),
    path('contents/delete-for-checked',
         views.DeleteNoteContentsForChecked.as_view(), name='StudyNoteAPIView'),
    path('contents/<int:content_pk>', views.StudyNoteContentView.as_view()),
    path('contents/<int:content_pk>/order-plus-one-for-note-content',
         views.order_plus_one_for_note_content.as_view()),  # order + 1
    path('contents/<int:content_pk>/order-minus-one-for-note-content',
         views.order_minus_one_for_note_content.as_view()),  # order + 1
    # 특정 노트의 contents 에 대한 crud

    path('<int:study_note_pk>/contents', views.StudyNoteContentsView.as_view()),
    path('<int:study_note_pk>/content/create-sub-title-for-page',
         views.CreateViewForSubTitleForNote.as_view()),

    path('<int:study_note_pk>/content/create-youtube-content-for-note',
         views.CreateViewForYoutubeContentForNote.as_view()),

    path('<int:study_note_pk>/content/get-subtitle-list',
         views.ApiViewForGetSubtitleListForNote.as_view()),


    path('<int:study_note_pk>/contents/delete-page',
         views.DeleteNoteContentsForSelectedPage.as_view()),  # 특정 노트의 페이지에 대해 delete


    path('<int:study_note_pk>/comment/get-comment-list', views.ListViewForStudyNoteBriefingBoard.as_view()),     


    # ${notePk}/register-for-co-writer
    path('<int:notePk>/register-for-co-writer',
         views.CreateViewForCoWriterForOhterUserNote.as_view(), name='api_docu_detail'),

    # 0528 페이지 업데이트 (왼쪽 클릭으로 여러개 선택 => 오른족 클릭으로 여러개 선택 => 이동)
    path('<int:study_note_pk>/contents/UpdateNoteContentsPageForSelected',
         views.UpdateNoteContentsPageForSelectedView.as_view()),

    # CoWriter/${pk}
    path('CoWriter/<int:co_writer_pk>',
         views.ApiViewForCoWriter.as_view()),

    path('<int:study_note_pk>/contents/minus-one-page-for-selected-page',
         views.MinusOnePageForSelectedPageForStudyNoteContents.as_view()),
    path('<int:study_note_pk>/contents/plus-one-page-for-selected-page',
         views.PlusOnePageForSelectedPageForStudyNoteContents.as_view()),
    path('create-dummy', views.AddDummyDataForStudyNote.as_view(),
         name='AddDummyDataForStudyNote'),
    path('create-dummy-content', views.StudyNoteContentDummyAPI.as_view(),
         name='AddDummyDataForStudyNote'),
    path('content/search', views.SearchContentListView.as_view()),

    # post
    path('copy-selected-notes-to-my-note',
         views.CopyCopySelectedNotesToMyNoteView.as_view()),

]
