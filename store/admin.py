from django.contrib import admin
from django.utils.html import format_html
from store.models import Category, Product, Brand
from reviews.admin import ReviewInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image_preview")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("image_preview",)

    fieldsets = ((None, {"fields": ("name", "slug", "image", "image_preview")}),)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                "<img src='{}' style='max-height: 100px;'/>", obj.image.url
            )
        return "-"

    image_preview.short_description = "Превью изображения"


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
        "review_count",
        "created_at",
        "image_preview",
    )
    list_filter = ("brand", "category", "color", "created_at", "updated_at")
    search_fields = ("name", "brand__name", "category__name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "rating",
        "review_count",
        "final_price_display",
        "image_preview",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    save_on_top = True

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "brand",
                    "category",
                    "description",
                    "image",
                    "image_preview",
                )
            },
        ),
        ("Ценообразование", {"fields": ("price", "discount", "final_price_display")}),
        ("Характеристики", {"fields": ("color", "rating")}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )
    inlines = [ReviewInline]

    def final_price_display(self, obj):
        return f"{obj.final_price():.2f} $"

    final_price_display.short_description = "Цена со скидкой"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return "-"

    image_preview.short_description = "Превью изображения"
