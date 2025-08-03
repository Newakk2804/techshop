from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_custom_email(subject, message, recipient_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=True,
    )