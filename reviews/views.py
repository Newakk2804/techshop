from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from reviews.forms import ReviewForm


@login_required
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == "POST":
        form = ReviewForm(request.POST, user=request.user, product=product)
        if form.is_valid():
            form.save()

    return redirect("store:detail_product", product_slug=product.slug)
