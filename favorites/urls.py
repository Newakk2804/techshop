from django.urls import path
from .views import toggle_wishlist


app_name = "store"

urlpatterns = [
    path("toggle/", toggle_wishlist, name="toggle_wishlist"),
]
