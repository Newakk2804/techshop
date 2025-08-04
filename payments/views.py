from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from orders.models import Order
from payments.models import Payment
from payments.paypal import paypalrestsdk


def start_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=False)
    payment = Payment.objects.create(
        order=order,
        amount=order.get_total_cost(),
        currency=settings.PAYPAL_CURRENCY,
        payment_method="paypal",
        status="pending",
    )

    paypal_payment = paypalrestsdk.Payment(
        {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    reverse("payments:payment_success", args=[payment.id])
                ),
                "cancel_url": request.build_absolute_uri(
                    reverse("payments:payment_cancel", args=[payment.id])
                ),
            },
            "transactions": [
                {
                    "amount": {
                        "total": str(payment.amount),
                        "currency": payment.currency,
                    },
                    "description": f"Оплата заказа #{order.id}",
                }
            ],
        }
    )

    if paypal_payment.create():
        payment.payment_id = paypal_payment.id
        payment.save()
        for link in paypal_payment.links:
            if link.method == "REDIRECT":

                return redirect(link.href)

        return redirect("orders:order_create")
    else:
        payment.status = "failed"
        payment.save()

        return redirect("orders:order_create")


def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    paypal_payment = paypalrestsdk.Payment.find(payment.payment_id)

    if paypal_payment.execute({"payer_id": request.GET.get("PayerID")}):
        payment.mark_as_paid()
        messages.success(request, "Оплата прошла успешно.")

        return redirect("orders:order_success", order_id=payment.order.id)
    else:
        payment.mark_as_failed()
        messages.error(request, "Ошибка при подтверждении оплаты.")

        return redirect("orders:order_create")


def payment_cancel(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.mar_as_cancelled()
    messages.warning(request, "Оплата была отменена.")

    return redirect("orders:order_create")
