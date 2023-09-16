from django.contrib import admin
from .models import (
    Challenge,
    EvaluationCriteria
)

# 127.0.0.1:8000/admin

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle',
                    'created_at_formatted', 'writer')


@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('item_description', 'challenge')
    list_filter = ('challenge',)
