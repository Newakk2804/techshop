from django.urls import path
from payments import views

app_name = "payments"

urlpatterns = [
    path("start/<int:order_id>/", views.start_payment, name="start_payment"),
    path("success/<int:payment_id>/", views.payment_success, name="payment_success"),
    path("cancel/<int:payment_id>/", views.payment_cancel, name="payment_cancel"),
]
