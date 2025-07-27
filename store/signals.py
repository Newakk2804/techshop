import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Product, Category
from newsletters.tasks import send_new_product_email_task


@receiver(post_save, sender=Product)
def trigger_product_email(sender, instance, created, **kwargs):
    if created:
        send_new_product_email_task.delay(instance.slug)


def delete_file(file_field):
    if file_field and file_field.name != "" and os.path.isfile(file_field.path):
        try:
            os.remove(file_field.path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    delete_file(instance.image)


@receiver(post_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    delete_file(instance.image)
