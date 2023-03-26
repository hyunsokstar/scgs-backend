# Register your models here.
from django.contrib import admin
from .models import ProjectProgress, SupplementaryTask


@admin.register(ProjectProgress)
class ProjectProgress(admin.ModelAdmin):
    list_display = (
        "pk",
        "task",
        "writer",
        "importance",
        "task_completed",
        "password",
    )

@admin.register(SupplementaryTask)
class SupplementaryTaskAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "task_manager",
        "task",
        "importance",
        "task_status",
    )
