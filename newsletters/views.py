from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber
import json


def subscribe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse(
                {"success": False, "error": "Почта обязательна"}, status=400
            )

        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse(
                {"success": False, "error": "Вы уже подписчик"}, status=400
            )

        Subscriber.objects.create(email=email)

        send_mail(
            subject="Вы успешно подписались на рассылку!",
            message="Спасибо за подписку на наши новости. Мы будем держать вас в курсе!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)
