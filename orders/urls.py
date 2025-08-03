from django.urls import path
from orders.views import order_create, order_success


app_name = "orders"

urlpatterns = [
    path("create/", order_create, name="order_create"),
    path("success/<int:order_id>/", order_success, name="order_success"),
]
