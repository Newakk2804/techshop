from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
import json
from .models import Favorite
from store.models import Product


@login_required
def favorite_list_view(request):
    favorites = Favorite.objects.select_related("product").filter(user=request.user)
    context = {
        "favorites": favorites,
    }

    return render(request, "favorites/favorites.html", context)


@require_POST
@login_required
def toggle_wishlist(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)
    product_id = data.get("product_id")

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user, product=product
    )

    if not created:
        favorite.delete()
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "added"})


@login_required
def favorite_count(request):
    count = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({"count": count})
