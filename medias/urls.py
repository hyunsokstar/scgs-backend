from django.urls import path
# from .views import CreateViewForRefImageToTaskDetail, DeleteViewForRefImageForTask, PhotoDetail, GetUploadURL, createTestImageResult,TestResultImageForExtraTask
from .views import (
    CreateViewForRefImageToTaskDetail,
    DeleteViewForRefImageForTask,
    PhotoDetail,
    GetUploadURL,
    createTestImageResult,
    TestResultImageForExtraTask,
    DeleteViewForRefImageForExtraTask
)

urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("ref-image-for-task/<int:pk>/delete",
         DeleteViewForRefImageForTask.as_view()),
    path("ref-image-for-extra-task/<int:pk>/delete",
         DeleteViewForRefImageForExtraTask.as_view()),
    path("ref-image-for-task/upload",
         CreateViewForRefImageToTaskDetail.as_view()),
    path("TestResultImageForExtraTask",
         TestResultImageForExtraTask.as_view()),
    path("test-result-image/create",
         createTestImageResult.as_view()),
]
