from django.contrib import admin
from .models import StudyNote, StudyNoteContent

@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'writer')

@admin.register(StudyNoteContent)
class StudyNoteContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file_name', 'writer', 'created_at',)
    list_filter = ('writer',)
    search_fields = ('title', 'file_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('study_note','title', 'file_name', 'content','page')
        }),
        ('Writer', {
            'fields': ('writer',)
        }),
        ('Time', {
            'fields': ('created_at',),
        }),
    )    
