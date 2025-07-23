from django.shortcuts import render
from .models import Category, Brand, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by("-created_at")[:5]
    context = {"categories": categories, "new_products": products}
    return render(request, "store/index.html", context)


def products_all(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by("-created_at")
    brands = Brand.objects.all()

    selected_category_ids = request.GET.getlist("category")
    if selected_category_ids:
        products = products.filter(category_id__in=selected_category_ids)

    context = {
        "categories": categories,
        "products": products,
        "brands": brands,
        "selected_category_ids": selected_category_ids,
    }
    return render(request, "store/store.html", context)


def product_filter_ajax(request):
    products = Product.objects.all().order_by("-created_at")

    category_ids = request.GET.getlist("category")
    brands_ids = request.GET.getlist("brand")
    price_min = request.GET.get("min_price")
    price_max = request.GET.get("max_price")

    if category_ids:
        products = products.filter(category_id__in=category_ids)

    if brands_ids:
        products = products.filter(brand_id__in=brands_ids)

    if price_min:
        products = products.filter(price__gte=price_min)

    if price_max:
        products = products.filter(price__lte=price_max)

    context = {"products": products}

    return render(request, "store/components/_product_list.html", context)


def detail_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    related_products = Product.objects.filter(category__name=product.category).exclude(
        name=product.name
    )
    print(related_products)
    print(product.category)
    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "store/detail_product.html", context)
