from django.shortcuts import get_object_or_404, render, redirect
from orders.models import Order, OrderItem
from orders.forms import OrderCreateForm
from carts.models import CartItem
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = request.user.get_cart_total_price()
    total_quantity = request.user.get_cart_total_quantity()

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.final_price(),
                    quantity=item.quantity,
                )

            cart_items.delete()

            return redirect("payments:start_payment", order_id=order.id)
    else:
        form = OrderCreateForm()

    context = {
        "form": form,
        "cart_items": cart_items,
        "total_price": total_price,
        "total_quantity": total_quantity,
    }

    return render(request, "orders/order_create.html", context)


def order_success(request, order_id):
    context = {"order_id": order_id}

    return render(request, "orders/order_success.html", context)


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "orders": orders,
    }

    return render(request, "orders/user_orders.html", context)


@login_required
def user_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        "order": order,
    }

    return render(request, "orders/user_order_detail.html", context)
