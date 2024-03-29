from django.urls import path
from . import views

urlpatterns = [
    path("", views.StudyNoteAPIView.as_view(), name="StudyNoteAPIView"),
    path(
        "content/move-contents-to-selected-page",
        views.UpdateViewForMoveNoteContentsToOtherPage.as_view(),
        name="StudyNoteAPIView",
    ),
    
    path("content/PageToPageContentReplacement", views.PageToPageContentReplacementView.as_view()),
    
    path("mybookmark", views.ListViewForMyBookMark.as_view()),
    path("my-like-note-list", views.ListViewForMyLikeNote.as_view()),
    path(
        "for-register-roadmap",
        views.StudyNoteAPIViewForRegisterRoadMap.as_view(),
        name="StudyNoteAPIView",
    ),
    path("<int:notePk>/<int:pageNum>", views.StudyNoteDetailView.as_view()),
    path("<int:notePk>", views.DeleteViewForStudyNote.as_view()),
    path("<int:notePk>/bookmark", views.BookMarkViewForNoteForPk.as_view()),
    path(
        "<int:my_note_id>/getSelectedNoteInfoAndPageNumberList",
        views.InfoViewForSelectedNoteInfoAndPageNumberList.as_view(),
    ),
    path("<int:notePk>/like", views.LikeViewForNoteForPk.as_view()),
    path(
        "comment/<int:commentPk>/delete", views.DeleteViewForStudyNoteComment.as_view()
    ),
    path(
        "comment/<int:commentPk>/update-comment",
        views.UpdateViewForStudyNoteComment.as_view(),
    ),
    path(
        "<int:studyNotePk>/create-comment", views.CreateViewForCommentForNote.as_view()
    ),
    path(
        "comment/<int:commentPk>/update-edit-mode",
        views.UpdateViewForEditModeForStudyNoteBriefingBoard.as_view(),
        name="StudyNoteAPIView",
    ),
    path(
        "update-is-approved-for-cowriter",
        views.UpdateViewForIsApprovedForCoWorker.as_view(),
    ),
    path(
        "get-study-note-list-for-copy-mode",
        views.StudyNoteAPIViewForCopyMode.as_view(),
        name="StudyNoteAPIView",
    ),
    path(
        "get-study-note-for-checked-rows/",
        views.StudyNoteAPIViewForCheckedRows.as_view(),
        name="StudyNoteAPIView",
    ),
    path("for-me/", views.StudyNoteAPIViewForMe.as_view()),
    path(
        "<int:pk>/contents/update/re-order-for-contents",
        views.StudyNoteContentReOrderAPIView.as_view(),
        name="study-note-contents-re-order",
    ),
    path(
        "contents/delete-for-checked",
        views.DeleteNoteContentsForChecked.as_view(),
        name="StudyNoteAPIView",
    ),
    #  content update view
    path("contents/<int:content_pk>", views.StudyNoteContentView.as_view()),
    path(
        "content/<int:content_pk>/update-subtitle",
        views.UpdateViewForNoteSubtitle.as_view(),
    ),
    path(
        "contents/<int:content_pk>/order-plus-one-for-note-content",
        views.order_plus_one_for_note_content.as_view(),
    ),  # order + 1
    path(
        "contents/<int:content_pk>/order-minus-one-for-note-content",
        views.order_minus_one_for_note_content.as_view(),
    ),  # order + 1
    # 특정 pk
    path("qa-board/<int:question_pk>/update", views.UpdateViewForQnABoard.as_view()),
    path(
        "qa-board/<int:question_pk>/delete", views.DeleteViewForQuestionBoard.as_view()
    ),
    #   질문에 댓글 추가
    path(
        "qa-board/<int:question_pk>/add-comment",
        views.CreateViewForCommentForQuestionForNote.as_view(),
    ),
    path(
        "answer-for-qaboard/<int:commentPk>/update-comment",
        views.UpdateViewForCommentForQuestionForNote.as_view(),
    ),
    path(
        "answer-for-qaboard/<int:commentPk>/delete-comment",
        views.DeleteViewForCommentForQuestionForNote.as_view(),
    ),
    path("<int:study_note_pk>/create-question", views.CreateViewForQnABoard.as_view()),
    path(
        "<int:study_note_pk>/create-error-report",
        views.CreateViewForErrorRecordForNote.as_view(),
    ),
    path(
        "<int:study_note_pk>/error-report-list",
        views.ErrorReportForStudyNoteView.as_view(),
    ),
    path(
        "<int:study_note_pk>/error-report/<int:page>",
        views.ErrorReportForPageForStudyNoteView.as_view(),
    ),
    path(
        "class-room/load-saved-page/<int:study_note_pk>",
        views.GetSavedPageForCurrentNote.as_view(),
    ),
    path(
        "error-report/<int:error_report_pk>/delete",
        views.DeleteViewForErrorReport.as_view(),
    ),
    path(
        "error-report/<int:error_report_pk>/update",
        views.UpdateViewForErrorReport.as_view(),
    ),
    path(
        "<int:study_note_pk>/content/create-sub-title-for-page",
        views.CreateViewForSubTitleForNote.as_view(),
    ),
    path(
        "<int:study_note_pk>/content/create-youtube-content-for-note",
        views.CreateViewForYoutubeContentForNote.as_view(),
    ),
    path(
        "<int:study_note_pk>/content/get-subtitle-list",
        views.ApiViewForGetSubtitleListForNote.as_view(),
    ),
    path(
        "<int:study_note_pk>/contents/delete-page",
        views.DeleteNoteContentsForSelectedPage.as_view(),
    ),  # 특정 노트의 페이지에 대해 delete
    path(
        "<int:study_note_pk>/comment/get-comment-list",
        views.ListViewForStudyNoteBriefingBoard.as_view(),
    ),
    # ${notePk}/register-for-co-writer
    path(
        "<int:notePk>/register-for-co-writer",
        views.CreateViewForCoWriterForOhterUserNote.as_view(),
        name="api_docu_detail",
    ),
    # 0528 페이지 업데이트 (왼쪽 클릭으로 여러개 선택 => 오른족 클릭으로 여러개 선택 => 이동)
    path(
        "<int:study_note_pk>/contents/UpdateNoteContentsPageForSelected",
        views.UpdateNoteContentsPageForSelectedView.as_view(),
    ),
    # CoWriter/${pk}
    path("CoWriter/<int:co_writer_pk>", views.ApiViewForCoWriter.as_view()),
    path(
        "<int:study_note_pk>/contents/minus-one-page-for-selected-page",
        views.MinusOnePageForSelectedPageForStudyNoteContents.as_view(),
    ),
    path(
        "<int:study_note_pk>/contents/plus-one-page-for-selected-page",
        views.PlusOnePageForSelectedPageForStudyNoteContents.as_view(),
    ),
    path(
        "create-dummy",
        views.AddDummyDataForStudyNote.as_view(),
        name="AddDummyDataForStudyNote",
    ),
    path(
        "create-dummy-content",
        views.StudyNoteContentDummyAPI.as_view(),
        name="AddDummyDataForStudyNote",
    ),
    path("content/search", views.SearchContentListView.as_view()),
    path("<int:study_note_pk>/contents", views.StudyNoteContentsView.as_view()),
    # create view
    path("roadmap/create", views.CreateViewForRoadMap.as_view()),
    path(
        "roadmap/register-from-checked-note-ids",
        views.CreateViewForRegisterRoadMapFromCheckedNoteIds.as_view(),
    ),
    #  deleteview
    path(
        "roadmap/content/delete-for-checked-ids",
        views.DeleteViewForRoadMapContentForCheckedIds.as_view(),
    ),
    # update view 1106
    path(
        "roadmap/content/order/update", views.UpdateViewForRoadMapContentOrder.as_view()
    ),
    path("<int:study_note_pk>/FAQBoard/add", views.CreteViewForFAQBoard.as_view()),
    path(
        "<int:study_note_pk>/suggestion/add",
        views.CreateViewForSuggestionForNote.as_view(),
    ),
    # list view
    path("roadmap", views.ListViewForRoadMap.as_view()),
    path("roadmap/<int:roadMapId>/content/", views.ListViewForRoadMapContent.as_view()),
    path(
        "roadmap/<int:roadMapId>/content/for-register",
        views.ListViewForRoadMapContentForRegister.as_view(),
    ),
    path("<int:study_note_pk>/class-room", views.ClasssRoomView.as_view()),
    path("<int:study_note_pk>/qa-list", views.QnABoardView.as_view()),
    path("<int:study_note_pk>/FAQBoard", views.FAQBoardView.as_view()),
    #  study-note/${study_note_pk}/suggestion
    path("<int:study_note_pk>/suggestion", views.ListViewForSuggestion.as_view()),
    # post
    path(
        "copy-selected-notes-to-my-note",
        views.CopyCopySelectedNotesToMyNoteView.as_view(),
    ),
    path("copy-one-of-note-to-me", views.CopyOneOfNoteToMe.as_view()),
    path(
        "<int:study_note_id>/GetMyNoteInfoAndTargetNoteInforToPartialCopy",
        views.GetMyNoteInfoAndTargetNoteInForToPartialCopy.as_view(),
    ),
    path(
        "error-report/<int:error_report_pk>/comment/add",
        views.CreateViewForErrorReportComment.as_view(),
    ),
    path(
        "faq-board/<int:faqPk>/comment/add",
        views.CreateViewForCommentForFaqBoard.as_view(),
    ),
    path(
        "suggestion/<int:suggestionPk>/comment/add",
        views.CreateViewForCommentForSuggestionForNote.as_view(),
    ),
    #     path('suggestion/<int:suggestionPk>/comment', views.ListViewForCommentForSuggestion.as_view()),
    # comment list view
    path(
        "suggestion/<int:suggestionPk>/comment",
        views.ListViewForCommentForSuggestion.as_view(),
    ),
    path(
        "faq-board/<int:faqPk>/comment", views.ListViewForCommentForFaqBoard.as_view()
    ),
    # search
    path("search", views.SearchViewForStudyNoteCardList.as_view()),
    path(
        "<int:study_note_pk>/faq/search", views.SearchViewForStudyNoteFaqList.as_view()
    ),
    path(
        "<int:study_note_pk>/suggestion/search",
        views.SearchViewForStudyNoteSuggestionList.as_view(),
    ),
    path(
        "<int:study_note_pk>/qna/search", views.SearchViewForStudyNoteQnaList.as_view()
    ),
    path(
        "<int:study_note_pk>/error-report/search",
        views.SearchViewForStudyNoteErrorReportList.as_view(),
    ),
    path("faq/<int:faq_pk>/update", views.UpdateViewForFaq.as_view()),
    path(
        "suggestion/<int:suggestionPk>/update", views.UpdateViewForSuggestion.as_view()
    ),
    # deleteview
    path(
        "<int:study_note_pk>/classroom/withdraw",
        views.DeleteViewForWithDrawClassRoom.as_view(),
    ),
    path("faq/<int:faq_pk>/delete", views.DeleteViewForNoteFaq.as_view()),
    # study-note/error-report/comment/${commentPk}/delete
    path(
        "error-report/comment/<int:commentPk>/delete",
        views.DeleteViewForCommentForErrorReport.as_view(),
    ),
    # classroom/${classRoomId}/delete
    path(
        "classroom/<int:classRoomId>/delete",
        views.DeleteViewForClassRoomForNote.as_view(),
    ),
    path(
        "faq-board/comment/<int:commentPk>/update",
        views.UpdateViewForFaqComment.as_view(),
    ),
    path(
        "suggestion/comment/<int:commentPk>/delete",
        views.DeleteViewForCommentForSuggestion.as_view(),
    ),
    # study-note/suggestion/comment/${commentPk}/update
    path(
        "suggestion/comment/<int:commentPk>/update",
        views.UpdateViewForSuggestionComment.as_view(),
    ),
    # comment delete view
    # roadmap/${roadMapId}/delete
    path("roadmap/<int:roadMapId>/delete", views.DeleteViewForRoadMap.as_view()),
    # faq-baord/${commentPk}/delete
    path(
        "faq-board/comment/<int:commentPk>/delete",
        views.DeleteViewForFaqComment.as_view(),
    ),
    # update view
    path(
        "<int:coWriterId>/update-is-tasking-for-cowriter",
        views.UpdateViewForIsTaskingForCowriter.as_view(),
    ),
]
