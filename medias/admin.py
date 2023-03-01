from django.contrib import admin
from .models import Photo, PhotoForProfile, Video

# Register your models here.

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
