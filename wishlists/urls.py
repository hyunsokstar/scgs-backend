from django.urls import path

from .views import Wishlists, WishlistDetail

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),    
]
