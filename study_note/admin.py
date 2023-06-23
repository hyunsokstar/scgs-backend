from django.contrib import admin
from .models import (
    StudyNote,
    StudyNoteBriefingBoard,
    StudyNoteContent,
    CoWriterForStudyNote,
    ClassRoomForStudyNote,
    QnABoard,
    AnswerForQaBoard
)


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'writer',
                    'first_category', 'second_category')


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
