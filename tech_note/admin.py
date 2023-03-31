from django.contrib import admin
from .models import TechNote, TechNoteContent


@admin.register(TechNote)
class TechNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author',
                    'like_count', 'view_count', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'author__username',)
    ordering = ('-created_at',)


@admin.register(TechNoteContent)
class TechNoteContentAdmin(admin.ModelAdmin):
    list_display = ('tech_note', 'title', 'file', 'content', 'created_at')
