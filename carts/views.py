from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import CartItem
from store.models import Product


@login_required
def cart_view(request):
    cart_items = request.user.cart_items.select_related("product")
    total_price = request.user.get_cart_total_price()
    total_quantity = request.user.get_cart_total_quantity()
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_quantity": total_quantity,
    }

    return render(request, "carts/cart.html", context)


@require_POST
@login_required
def add_to_cart(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    product_it = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = Product.objects.get(id=product_it)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1 if quantity <= 0 else quantity},
    )

    if not created:
        cart_item.quantity += 1 if quantity <= 0 else quantity
        cart_item.save()

    return JsonResponse({"success": True})


@require_POST
@login_required
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        cart_item_id = data.get("cart_item_id")

        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()

        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.get_total_price() for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)

        return JsonResponse(
            {
                "success": True,
                "total_price": total_price,
                "total_quantity": total_quantity,
            }
        )
    except CartItem.DoesNotExist:
        return JsonResponse({"success": False, "error": "Item not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
def cart_count(request):
    count = request.user.get_cart_total_quantity()
    return JsonResponse({"count": count})
