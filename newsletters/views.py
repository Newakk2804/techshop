from django.http import JsonResponse
from .models import Subscriber
from .tasks import send_subscription_email
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

        send_subscription_email.delay(email)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)
