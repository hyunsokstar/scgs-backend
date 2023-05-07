from django.contrib import admin
from .models import LongTermPlan

@admin.register(LongTermPlan)
class LongTermPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'writer', 'created_at')
    list_filter = ('category', 'writer')
    search_fields = ('title', 'description', 'writer__username')
