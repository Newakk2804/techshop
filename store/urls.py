from django.urls import path
from .views import detail_product, index, products_all, product_filter_ajax


app_name = "store"

urlpatterns = [
    path("", index, name="index"),
    path("products/", products_all, name="products"),
    path("products/ajax/", product_filter_ajax, name="product_filter_ajax"),
    path("detail-product/<slug:product_slug>", detail_product, name="detail_product"),
]
