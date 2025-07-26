from django.urls import path
from .views import subscribe


app_name = "newsletters"

urlpatterns = [
    path("subscribe/", subscribe, name="subscribe"),
]
