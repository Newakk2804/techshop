from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    subscribed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата подписки"
    )

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return self.email
