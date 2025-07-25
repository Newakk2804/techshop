from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls", namespace="store")),
    path("auth/", include("accounts.urls", namespace="auth")),
    path("favorite/", include("favorites.urls", namespace="favorite")),
    path("cart/", include("carts.urls", namespace="cart")),
    path("newsletters/", include("newsletters.urls", namespace="newsletters")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
