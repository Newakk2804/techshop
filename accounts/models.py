from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def get_cart_total_price(self):
        return sum(item.get_total_price() for item in self.cart_items.all())

    def get_cart_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())
