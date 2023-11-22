from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SkillForFrameWork, UserPosition, UserTaskComment
from django.utils import timezone

# Register your models here.


@admin.register(UserTaskComment)
class UserTaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'comment', 'like_count',
                    'created_at_formatted')
    search_fields = ('writer__username', 'comment')

    def has_add_permission(self, request):
        return True


@admin.register(UserPosition)
class UserPositionAdmin(admin.ModelAdmin):
    list_display = ("pk", "position_name")


@admin.register(SkillForFrameWork)
class SkillForFrameWorkAdmin(admin.ModelAdmin):
    list_display = ("pk", "frame_work_name")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "password",
                    "name",
                    "email",
                    'skill_for_frameWork',
                    'position',
                    'about_me',
                    'admin_level',
                    'profile_image',
                    'cash'
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = ["pk", "username", "password", "name", "email"]
