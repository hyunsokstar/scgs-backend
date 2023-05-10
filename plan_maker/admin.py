from django.contrib import admin
from .models import LongTermPlan, LongTermPlanContents


@admin.register(LongTermPlan)
class LongTermPlanAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',
                    'category', 'writer', 'created_at')
    list_filter = ('category', 'writer')
    search_fields = ('title', 'description', 'writer__username')


@admin.register(LongTermPlanContents)
class LongTermPlanContentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'long_term_plan', 'name', 'start', 'end',
                    'progress', 'dependencies', 'displayOrder')
    list_filter = ()
    search_fields = ('name',)
    ordering = ('-start',)
    fieldsets = (
        (None, {
            'fields': ('long_term_plan', 'name',  'dependencies')
        }),
        ('기간 정보', {
            'fields': ('start', 'end')
        }),
        ('진행률', {
            'fields': ('progress',)
        }),
    )
