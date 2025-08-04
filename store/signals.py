import os
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from store.models import Product, Category
from reviews.models import Review
from newsletters.tasks import send_new_product_email_task
from django.core.cache import cache


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


@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    reviews = product.reviews.all()
    agg = reviews.aggregate(avg=Avg("rating"), count=Count("id"))

    product.rating = round(agg["avg"] or 0, 1)
    product.review_count = agg["count"]
    product.save()


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache_key = f"product_detail_{instance.slug}"
    cache.delete(cache_key)
