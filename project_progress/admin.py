# Register your models here.
from django.contrib import admin
from .models import ProjectProgress, ExtraTask, TaskComment, TestForTask, TestersForTest, TaskLog


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "task_manager",
        "writer",
        "task",
        "task_description",
        "importance",
        "task_completed",
        "password",
        "due_date_option"
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


@admin.register(TestersForTest)
class TechNoteTesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'tester', 'created_at')
    list_filter = ('test', 'created_at')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "writer", "comment",
                    "like_count", "created_at")
    list_filter = ("task", "writer", "created_at")
    search_fields = ("comment",)
    ordering = ("-created_at",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "task":
            kwargs["queryset"] = ProjectProgress.objects.filter(
                task_completed=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'task', 'completed_at', "interval_between_team_task",
                    "interval_between_my_task")  # Admin 목록에 표시할 필드 설정
    list_filter = ('writer',)  # 필터 옵션 설정
    search_fields = ('task',)
