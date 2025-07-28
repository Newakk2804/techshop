from django.db import models
from store.models import Product
from django.conf import settings


class Review(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Продукт",
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("product", "user")

    def __str__(self):
        return (
            f"Review by {self.user.username} on {self.product.name} ({self.rating}⭐)"
        )
