# Register your models here.
from django.contrib import admin
from .models import (
    ProjectProgress, ExtraTask, TaskComment,
    TestForTask, TestersForTest, TaskLog,
    TaskUrlForTask, TaskUrlForExtraTask,
    ExtraTaskComment, TestForExtraTask,
    TestersForTestForExtraTask
)


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'task_manager',
        'task_classification',
        'current_status',
        'due_date',
    )
    list_filter = (
        'task_classification',
        'current_status',
    )
    search_fields = (
        'task',
        'task_manager__username',
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
    list_display = ('id', 'writer', 'task', 'completed_at',
                    "interval_between_team_task",
                    "interval_between_my_task",
                    "time_distance_for_team_task",
                    "time_distance_for_my_task"
                    )  # Admin 목록에 표시할 필드 설정
    list_filter = ('writer',)  # 필터 옵션 설정
    search_fields = ('task',)


@admin.register(TaskUrlForTask)
class TaskUrlForTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'task_url', 'task_description')
    search_fields = ('task_url', )

# Task url for extra tasks


@admin.register(TaskUrlForExtraTask)
class TaskUrlForExtraTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "task_url", "task_description")
    list_filter = ("task",)
    search_fields = ("task__name",)


@admin.register(ExtraTaskComment)
class ExtraTaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'writer', 'comment',
                    'like_count', 'created_at_formatted', 'is_edit_mode')
    list_filter = ('task', 'writer', 'is_edit_mode')
    search_fields = ('comment', 'writer__username')
    readonly_fields = ('created_at',)

    def created_at_formatted(self, obj):
        if obj.created_at is not None:
            local_created_at = obj.created_at.astimezone()
            return local_created_at.strftime('%y년 %m월 %d일 %H시 %M분')
        else:
            return "준비"

    created_at_formatted.short_description = 'Created At'


@admin.register(TestForExtraTask)
class TestForExtraTaskAdmin(admin.ModelAdmin):
    list_display = ("test_description", "original_task", "test_passed")
    list_filter = ("test_passed", "test_method")
    search_fields = ("test_description", "original_task__name")

    fieldsets = (
        ("General", {
            "fields": ("test_description", "original_task", "test_passed")
        }),
        ("Details", {
            "fields": ("test_method", "test_result_image")
        }),
    )


@admin.register(TestersForTestForExtraTask)
class TestersForTestForExtraTaskAdmin(admin.ModelAdmin):
    list_display = ('test', 'tester', 'created_at')
    list_filter = ('test', 'tester')
    search_fields = ('test__name', 'tester__username')
    fields = ('test', 'tester')
