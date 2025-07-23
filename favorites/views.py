from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Favorite
from store.models import Product


@require_POST
@login_required
def toggle_wishlist(request):
    data = json.loads(request.body)
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
