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
    CommentForErrorReport
)


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'writer',
                    'first_category', 'second_category')


@admin.register(ErrorReportForStudyNote)
class ErrorReportForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ['study_note', 'writer', 'page', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['study_note__title', 'writer__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(StudyNoteContent)
class StudyNoteContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file_name',
                    'writer', 'order', 'content_option', 'created_at',)
    list_filter = ('writer',)
    search_fields = ('title', 'file_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields':
            ('study_note', 'title', 'file_name',
             'content', 'order', 'page', "content_option", "youtube_url")
        }),
        ('Writer', {
            'fields': ('writer',)
        }),
        ('Time', {
            'fields': ('created_at',),
        }),
    )


@admin.register(CoWriterForStudyNote)
class CoWriterForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ('writer', 'study_note', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('writer__username', 'study_note__title')
    readonly_fields = ('created_at',)


@admin.register(StudyNoteBriefingBoard)
class StudyNoteBriefingBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'writer', 'comment', 'like_count',
                    'created_at_formatted', 'updated_at', 'is_edit_mode')
    list_filter = ('is_edit_mode',)
    search_fields = ('comment',)


@admin.register(ClassRoomForStudyNote)
class ClassRoomForStudyNoteAdmin(admin.ModelAdmin):
    list_display = ['current_note', 'current_page',
                    'writer', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['current_note__title', 'writer__username']


@admin.register(QnABoard)
class QnABoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'writer', 'created_at', 'updated_at']
    list_filter = ['writer', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']



@admin.register(AnswerForQaBoard)
class AnswerForQaBoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'writer', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question__title', 'writer__username']    

@admin.register(FAQBoard)
class FAQBoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "study_note",  "writer", "created_at")
    list_filter = ("study_note", "writer", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_at_formatted")

    fieldsets = (
        ("FAQ 정보", {
            "fields": ("study_note", "title", "content", "page", "writer")
        }),
        ("시간 정보", {
            "fields": ("created_at", "updated_at", "created_at_formatted"),
            "classes": ("collapse",)
        }),
    )
    
    def created_at_formatted(self, obj):
        return obj.created_at_formatted()
    created_at_formatted.short_description = "작성일시"

admin.site.site_header = "FAQBoard 관리"
admin.site.site_title = "FAQBoard 관리"

@admin.register(CommentForErrorReport)
class CommentForErrorReportAdmin(admin.ModelAdmin):
    list_display = ('error_report', 'writer', 'created_at')
    list_filter = ('error_report', 'created_at')
    search_fields = ('error_report__study_note__title', 'writer__username', 'content')
    date_hierarchy = 'created_at'