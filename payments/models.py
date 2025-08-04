from django.db import models
from django.conf import settings
from orders.models import Order
from django.utils import timezone


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Ожидает оплаты"),
        ("completed", "Оплачен"),
        ("failed", "Ошибка"),
        ("cancelled", "Отменен"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("paypal", "PayPal"),
        ("card", "Банковская карта"),
        ("cash", "Наличные"),
    )

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Заказ",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    currency = models.CharField(max_length=3, default="BYN", verbose_name="Валюта")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        verbose_name="Статус платежа",
    )
    payment_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="ID платежа"
    )
    transaction_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="ID транзакции"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Платеж #{self.id} для заказа #{self.order.id}"

    def mark_as_paid(self):
        self.status = "completed"
        self.paid_at = timezone.now()
        self.save()

        self.order.paid = True
        self.order.payment_id = self.payment_id
        self.order.save()

    def mark_as_cancelled(self):
        self.status = "cancelled"
        self.save()
