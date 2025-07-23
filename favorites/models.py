from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.conf import settings

class Favorite(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Продукт",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
