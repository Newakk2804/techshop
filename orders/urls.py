from django.urls import path
from orders.views import order_create, order_success, user_orders, user_order_detail


app_name = "orders"

urlpatterns = [
    path("create/", order_create, name="order_create"),
    path("success/<int:order_id>/", order_success, name="order_success"),
    path("my-orders/", user_orders, name="user_orders"),
    path("my-orders/<int:order_id>/", user_order_detail, name="user_order_detail"),
]
