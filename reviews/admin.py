from django.contrib import admin
from django.utils.html import format_html
from reviews.models import Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("user", "created_at")
    fields = ("user", "rating", "comment", "created_at")
    can_delete = True
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product_link",
        "user_link",
        "star_rating",
        "short_comment",
        "created_at",
    )
    list_filter = ("rating", "created_at", "product")
    search_fields = ("user__username", "product__name", "comment")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product", "user")
    ordering = ("created_at",)

    def product_link(self, obj):
        return format_html(
            "<a href='/admin/store/product/{}/change/'>{}</a>",
            str(obj.product.id),
            obj.product.name,
        )

    product_link.short_description = "Продукт"
    product_link.admin_order_field = "product"

    def user_link(self, obj):
        return format_html(
            "<a href='/admin/accounts/customuser/{}/change/'>{}</a>",
            str(obj.user.id),
            obj.user.username,
        )

    user_link.short_description = "Пользователь"
    user_link.admin_order_field = "user"

    def star_rating(self, obj):
        return format_html("★" + str(obj.rating) + "☆" * (5 - obj.rating))

    star_rating.short_description = "Рейтинг"

    def short_comment(self, obj):
        return (obj.comment[0:40] + "...") if len(obj.comment) > 40 else obj.comment

    short_comment.short_description = "Комментарий"
