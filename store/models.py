from django.db import models
from decimal import Decimal, ROUND_HALF_UP


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to="category/", blank=True, null=True, verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Product(models.Model):
    COLOR_CHOICES = [
        ("black", "Черный"),
        ("white", "Белый"),
        ("gray", "Серый"),
        ("silver", "Серебристый"),
        ("gold", "Золотой"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True)
    brand = models.ForeignKey(
        to=Brand,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Бренд",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    discount = models.PositiveIntegerField(default=0, verbose_name="Скидка в %")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name="Цвет")
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def final_price(self):
        if self.price is None or self.discount is None:
            return Decimal("0.00")
        final = self.price * (Decimal("1") - Decimal(self.discount) / Decimal("100"))
        return final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return self.name
