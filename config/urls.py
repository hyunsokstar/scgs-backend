from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("categories", include("categories.urls"))
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),    
    path("api/v1/estimates/", include("estimate.urls")),    
    path("api/v1/tutorials/", include("tutorials.urls")), 
    path("api/v1/project_progress/", include("project_progress.urls")), 
    path("api/v1/tech_note/", include("tech_note.urls")), 
    path("api/v1/api_docu/", include("api_docu.urls")), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
