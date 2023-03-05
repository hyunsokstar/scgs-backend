from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SkillForFrameWork, UserPosition

# Register your models here.

@admin.register(UserPosition)
class UserPositionAdmin(admin.ModelAdmin):
    list_display= ("pk","position_name")

@admin.register(SkillForFrameWork)
class SkillForFrameWorkAdmin(admin.ModelAdmin):
    list_display= ("pk","frame_work_name")

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
    list_display = ["username", "password", "name", "email"]
