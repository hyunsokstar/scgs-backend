# shortcut1
from django.contrib import admin
from .models import ShortCut, RelatedShortcut, Tags


class TagsInline(admin.TabularInline):
    model = ShortCut.tags.through


@admin.register(ShortCut)
class ShortCutAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'description', 'classification', 'writer')
    list_filter = ('classification', 'writer')
    search_fields = ('shortcut', 'description')


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
