from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from newsletters.tasks import send_new_product_email_task


@receiver(post_save, sender=Product)
def trigger_product_email(sender, instance, created, **kwargs):
    if created:
        send_new_product_email_task.delay(instance.slug)