from django.contrib import admin
from .models import Photo, Video

# Register your models here.

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
