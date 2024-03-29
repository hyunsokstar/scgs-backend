from django.contrib import admin
from .models import (
    StudyNote,
    StudyNoteBriefingBoard,
    StudyNoteContent,
    CoWriterForStudyNote,
    ClassRoomForStudyNote,
    QnABoard,
    AnswerForQaBoard,
    ErrorReportForStudyNote,
    FAQBoard,
    CommentForErrorReport,
    Suggestion,
    CommentForSuggestion,
    CommentForFaqBoard,
    RoadMap,
    RoadMapContent,
    BookMarkForStudyNote,
    LikeForStudyNote
)

# 1122
@admin.register(RoadMapContent)
class RoadMapContentAdmin(admin.ModelAdmin):
    list_display = (
        "study_note",
        "road_map",
        "writer",
        "created_at",
    )  # 모델 리스트에서 보여질 필드들
    list_filter = ("writer", "created_at")  # 필터링할 수 있는 필드들
    search_fields = ("study_note__title",)


@admin.register(RoadMap)
class RoadMapAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sub_title", "writer")  # admin 목록에 표시할 필드 설정
    list_filter = ("writer",)  # 필터 설정
    search_fields = ("title", "sub_title", "writer__username")  # 검색 설정
    # raw_id_fields = ('writer',)  # 외래키 필드를 선택 상자 대신 검색 상자로 표시


@admin.register(CommentForFaqBoard)
class CommentForFaqBoardAdmin(admin.ModelAdmin):
    list_display = ("writer", "content", "created_at")


@admin.register(CommentForSuggestion)
class CommentForSuggestionAdmin(admin.ModelAdmin):
    list_display = ("writer", "content", "created_at")


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "created_at")


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "writer",
        "first_category",
        "second_category",
    )


@admin.register(ErrorReportForStudyNote)
class ErrorReportForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ["study_note", "writer", "page", "is_resolved", "created_at"]
    list_filter = ["is_resolved", "created_at"]
    search_fields = ["study_note__title", "writer__username"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(StudyNoteContent)
class StudyNoteContentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "file_name",
        "writer",
        "order",
        "content_option",
        "created_at",
    )
    list_filter = ("writer",)
    search_fields = (
        "title",
        "file_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "study_note",
                    "title",
                    "file_name",
                    "content",
                    "order",
                    "page",
                    "content_option",
                    "youtube_url",
                )
            },
        ),
        ("Writer", {"fields": ("writer",)}),
        (
            "Time",
            {
                "fields": ("created_at",),
            },
        ),
    )


@admin.register(CoWriterForStudyNote)
class CoWriterForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "writer", "study_note", "is_tasking")
    list_filter = ("is_approved", "created_at")
    search_fields = ("writer__username", "study_note__title")
    readonly_fields = ("created_at",)


@admin.register(StudyNoteBriefingBoard)
class StudyNoteBriefingBoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "note",
        "writer",
        "comment",
        "like_count",
        "created_at_formatted",
        "updated_at",
        "is_edit_mode",
    )
    list_filter = ("is_edit_mode",)
    search_fields = ("comment",)


@admin.register(ClassRoomForStudyNote)
class ClassRoomForStudyNoteAdmin(admin.ModelAdmin):
    list_display = [
        "current_note",
        "current_page",
        "writer",
        "is_approved",
        "created_at",
    ]
    list_filter = ["is_approved", "created_at"]
    search_fields = ["current_note__title", "writer__username"]


@admin.register(QnABoard)
class QnABoardAdmin(admin.ModelAdmin):
    list_display = ["title", "writer", "created_at", "updated_at"]
    list_filter = ["writer", "created_at"]
    search_fields = ["title", "content"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(AnswerForQaBoard)
class AnswerForQaBoardAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "writer", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["question__title", "writer__username"]


@admin.register(FAQBoard)
class FAQBoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "study_note", "writer", "created_at")
    list_filter = ("study_note", "writer", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_at_formatted")

    fieldsets = (
        ("FAQ 정보", {"fields": ("study_note", "title", "content", "page", "writer")}),
        (
            "시간 정보",
            {
                "fields": ("created_at", "updated_at", "created_at_formatted"),
                "classes": ("collapse",),
            },
        ),
    )

    def created_at_formatted(self, obj):
        return obj.created_at_formatted()

    created_at_formatted.short_description = "작성일시"


@admin.register(CommentForErrorReport)
class CommentForErrorReportAdmin(admin.ModelAdmin):
    list_display = ("error_report", "writer", "created_at")
    list_filter = ("error_report", "created_at")
    search_fields = ("error_report__study_note__title", "writer__username", "content")
    date_hierarchy = "created_at"

@admin.register(BookMarkForStudyNote)
class BookMarkForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_note', 'bookmarked_at')
    list_filter = ('user', 'study_note', 'bookmarked_at')
    search_fields = ('user__username', 'study_note__title')

@admin.register(LikeForStudyNote)
class LikeForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_note', 'liked_at')  # 관리자 페이지에서 보여줄 필드 설정
    list_filter = ('liked_at',)  # 필터링할 수 있는 필드 설정
    search_fields = ('user__username', 'study_note__title')  # 검색 기능을 위한 필드 설정