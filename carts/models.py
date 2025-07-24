from django.db import models
from django.conf import settings
from store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Пользователь")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        return self.product.final_price() * self.quantity