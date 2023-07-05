from django.contrib import admin
from .models import (
    Photo,
    PhotoForProfile,
    ReferImageForTask,
    TestResultImageForTask,
    Video,
    TestResultImageForExtraTask,
    ReferImageForExtraTask,
    TestResultImageForCompletedTask
)

# Register your models here.


@admin.register(TestResultImageForCompletedTask)
class TestResultImageForCompletedTaskAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'task']


@admin.register(PhotoForProfile)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "user",
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "description",
        "room",
        "experience",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferImageForTask)
class ReferImageForTaskAdmin(admin.ModelAdmin):
    list_display = ("image_url", "task")


@admin.register(ReferImageForExtraTask)
class ReferImageForExtraTaskAdmin(admin.ModelAdmin):
    list_display = ("image_url", "task")


@admin.register(TestResultImageForTask)
class TestResultImageForTaskAdmin(admin.ModelAdmin):
    list_display = ("image_url", "test")


@admin.register(TestResultImageForExtraTask)
class TestResultImageForExtraTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'image_url')
    list_filter = ('test',)
    search_fields = ('test__name',)
    fields = ('test', 'image_url')
