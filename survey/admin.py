from django.contrib import admin
from .models import Survey, SurveyOption, SurveyAnswer

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'description')
    list_filter = ('writer',)
    search_fields = ('title',)

@admin.register(SurveyOption)
class SurveyOptionAdmin(admin.ModelAdmin):
    list_display = ('content', 'survey')
    list_filter = ('survey',)
    search_fields = ('content',)

@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('writer', 'survey', 'selected_option')
    list_filter = ('writer', 'survey')
    search_fields = ('writer__username', 'survey__title')