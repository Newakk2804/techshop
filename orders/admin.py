from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity", "get_cost")
    can_delete = False

    def get_cost(self, obj):
        return obj.get_cost()

    get_cost.short_description = "Стоимость"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "phone",
        "status",
        "paid",
        "created_at",
        "get_total_quantity",
        "get_total_cost",
    )
    list_filter = ("status", "paid", "created_at")
    search_fields = ("full_name", "email", "phone", "id")
    readonly_fields = ("created_at", "updated_at", "payment_id")
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {"fields": ("user", "full_name", "email", "phone", "address")}),
        ("Статус и оплата", {"fields": ("status", "paid", "payment_id")}),
        ("Время", {"fields": ("created_at", "updated_at")}),
    )

    def get_total_cost(self, obj):
        return obj.get_total_cost()

    get_total_cost.short_description = "Общая стоимость"

    def get_total_quantity(self, obj):
        return obj.get_total_quantity()

    get_total_quantity.short_description = "Общее количество"
