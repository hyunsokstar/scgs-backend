from django.contrib import admin
from .models import TechNote

@admin.register(TechNote)
class TechNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author',
                    'like_count', 'view_count', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'author__username',)
    ordering = ('-created_at',)
