from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, cart_count


app_name = "cart"

urlpatterns = [
    path("", cart_view, name="cart"),
    path("add/", add_to_cart, name="add_to_cart"),
    path("remove/", remove_from_cart, name="remove_from_cart"),
    path("count/", cart_count, name="cart_count"),
]
