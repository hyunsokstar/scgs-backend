from django.contrib import admin
from .models import (
    Suggestion,
    CommentForSuggestion,
    FAQBoard
)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content', 'writer__username')
    list_per_page = 20


@admin.register(CommentForSuggestion)
class CommentForSuggestionAdmin(admin.ModelAdmin):
    list_display = ('writer', 'content', 'created_at')


@admin.register(FAQBoard)
class FAQBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'writer')

    # 나머지 필드 설정 (필요한 경우)
