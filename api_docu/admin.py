from django.contrib import admin
from .models import ApiDocu

@admin.register(ApiDocu)
class ApiDocuAdmin(admin.ModelAdmin):
    list_display = ('id', 'classification', 'url', 'description')
    list_filter = ('classification',)
    search_fields = ('url', 'description')