from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Product
from newsletters.models import Subscriber
from django.core.mail import EmailMessage
from django.templatetags.static import static
from django.urls import reverse
from django.conf import settings


@receiver(post_save, sender=Product)
def send_new_product_email(sender, instance, created, **kwargs):
    if not created:
        return

    subscribers = Subscriber.objects.values_list("email", flat=True)
    if not subscribers:
        return

    site_url = settings.DOMAIN
    product_url = site_url + reverse("store:detail_product", args=[instance.slug])

    html_content = render_to_string(
        "store/emails/new_product_email.html",
        {
            "product": instance,
            "product_url": product_url,
        },
    )

    email = EmailMessage(
        subject=f"🆕 Новый товар: {instance.name}",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    email.content_subtype = "html"
    email.send()
