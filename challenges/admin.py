from django.contrib import admin
from .models import (
    Challenge,
    EvaluationCriteria,
    EvaluationResult,
    ChallengeResult
)

# 1122
@admin.register(EvaluationResult)
class EvaluationResultAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'challenger',
                    'evaluate_criteria_description', 'result')
    list_filter = ('result', 'challenge')
    search_fields = ('user__username', 'evaluate_criteria_description')
    actions = ['mark_pass', 'mark_fail', 'mark_undecided']

    def mark_pass(self, request, queryset):
        queryset.update(result='pass')

    mark_pass.short_description = "Mark selected as Pass"

    def mark_fail(self, request, queryset):
        queryset.update(result='fail')

    mark_fail.short_description = "Mark selected as Fail"

    def mark_undecided(self, request, queryset):
        queryset.update(result='undecided')

    mark_undecided.short_description = "Mark selected as Undecided"


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle',
                    'created_at_formatted', 'writer')


@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('item_description', 'challenge')
    list_filter = ('challenge',)


@admin.register(ChallengeResult)
class ChallengeResultAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'pass_status', 'created_at_formatted')
    # list_filter = ('pass_status',)
    # search_fields = ('challenge__title',)
