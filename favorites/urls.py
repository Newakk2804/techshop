from django.urls import path
from .views import toggle_wishlist, favorite_list_view, favorite_count


app_name = "favorites"

urlpatterns = [
    path("", favorite_list_view, name="list"),
    path("toggle/", toggle_wishlist, name="toggle_wishlist"),
    path("count/", favorite_count, name="count"),
]
