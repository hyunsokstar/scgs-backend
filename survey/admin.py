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


# Selected option 이 survey 에 속하는것들만 선택 할수 있게
@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('participant', 'survey', 'selected_option')
    list_filter = ('participant', 'survey')
    search_fields = ('participant__username', 'survey__title')