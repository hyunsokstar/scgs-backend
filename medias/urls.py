from django.urls import path
from .views import CreateViewForRefImageToTaskDetail, PhotoDetail, GetUploadURL

urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("ref-image-for-task/upload",
         CreateViewForRefImageToTaskDetail.as_view())
]
