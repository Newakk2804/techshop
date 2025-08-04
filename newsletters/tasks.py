from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from newsletters.models import Subscriber
from store.models import Product


@shared_task
def send_new_product_email_task(product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        return

    subscribers = Subscriber.objects.values_list("email", flat=True)
    if not subscribers:
        return

    site_url = settings.DOMAIN
    product_url = site_url + reverse("store:detail_product", args=[product.slug])

    html_content = render_to_string(
        "store/emails/new_product_email.html",
        {
            "product": product,
            "product_url": product_url,
        },
    )

    email = EmailMessage(
        subject=f"🆕 Новый товар: {product.name}",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=list(subscribers),
    )

    email.content_subtype = "html"
    email.send()


@shared_task
def send_subscription_email(email):
    send_mail(
        subject="Вы успешно подписались на рассылку!",
        message="Спасибо за подписку на наши новости. Мы будем держать вас в курсе!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )
