# shortcut/admin.py

from django.contrib import admin
from .models import ShortCut

class ShortCutAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'description', 'classification', 'writer')
    list_filter = ('classification', 'writer')
    search_fields = ('shortcut', 'description')

admin.site.register(ShortCut, ShortCutAdmin)