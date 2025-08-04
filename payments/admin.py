from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "amount",
        "currency",
        "payment_method",
        "status",
        "created_at",
        "paid_at",
    )
    list_filter = ("status", "payment_method", "currency", "created_at")
    search_fields = ("order__id", "payment_id", "transaction_id")
    readonly_fields = ("created_at", "updated_at", "paid_at")
