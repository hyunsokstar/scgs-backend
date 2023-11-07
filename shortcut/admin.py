# shortcut1
from django.contrib import admin
from .models import ShortCut, RelatedShortcut, Tags, ShortCutHub


class TagsInline(admin.TabularInline):
    model = ShortCut.tags.through


@admin.register(ShortCut)
class ShortCutAdmin(admin.ModelAdmin):
    list_display = ('description', 'classification', 'writer')
    list_filter = ('classification', 'writer')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [TagsInline]


@admin.register(RelatedShortcut)
class RelatedShortcutAdmin(admin.ModelAdmin):
    list_display = ['shortcut', 'shortcut_content',
                    'description', 'created_at']
    search_fields = ['shortcut_content', 'shortcut__name']
    list_filter = ['created_at']

@admin.register(ShortCutHub)
class ShortCutHubAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'writer', 'created_at')
    list_filter = ('writer', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'