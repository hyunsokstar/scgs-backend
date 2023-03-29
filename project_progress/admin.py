# Register your models here.
from django.contrib import admin
from .models import ProjectProgress, ExtraTask, TestForTask


@admin.register(ProjectProgress)
class ProjectProgress(admin.ModelAdmin):
    list_display = (
        "pk",
        "task",
        "task_description",
        "writer",
        "importance",
        "task_completed",
        "password",
    )


@admin.register(ExtraTask)
class ExtraTaskAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "task_manager",
        "task",
        "importance",
        "task_status"
    )

@admin.register(TestForTask)
class TestForTaskAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "test_description",
        "test_passed"
    )
