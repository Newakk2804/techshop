from django.contrib import admin
from .models import Category, Product, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "price",
        "discount",
        "final_price_display",
        "color",
        "rating",
        "created_at",
    )
    list_filter = ("brand", "category", "color", "created_at", "updated_at")
    search_fields = ("name", "brand__name", "category__name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "final_price_display")
    list_editable = ("price", "discount", "color", "rating")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    save_on_top = True

    fieldsets = (
        (
            None,
            {"fields": ("name", "slug", "brand", "category", "description", "image")},
        ),
        ("Ценообразование", {"fields": ("price", "discount", "final_price_display")}),
        ("Характеристики", {"fields": ("color", "rating")}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )

    def final_price_display(self, obj):
        return f"{obj.final_price():.2f} BYN"

    final_price_display.short_description = "Цена со скидкой"
