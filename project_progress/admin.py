# Register your models here.
from django.contrib import admin
from .models import ProjectProgress


@admin.register(ProjectProgress)
class ProjectProgress(admin.ModelAdmin):
    list_display = (
        "task",
        "writer",
        "importance",
        "task_completed",
        "password",
    )
