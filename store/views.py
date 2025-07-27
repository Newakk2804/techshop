from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Brand, Product
from .utils import paginatore_objects


def index(request):
    products = Product.objects.all().order_by("-created_at")[:5]
    context = {"new_products": products}
    return render(request, "store/index.html", context)


def products_all(request):
    products = Product.objects.all().order_by("-created_at")
    brands = Brand.objects.all()

    selected_category_ids = request.GET.getlist("category")
    if selected_category_ids:
        products = products.filter(category_id__in=selected_category_ids)

    query = request.GET.get("q", "")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    page_obj = paginatore_objects(request, products, per_page=12)

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "brands": brands,
        "selected_category_ids": selected_category_ids,
        "query": query,
    }
    return render(request, "store/store.html", context)


def product_filter_ajax(request):
    try:
        products = Product.objects.all().order_by("-created_at")

        category_ids = request.GET.getlist("category")
        brands_ids = request.GET.getlist("brand")
        price_min = request.GET.get("min_price")
        price_max = request.GET.get("max_price")
        query = request.GET.get("q", "").strip()

        if category_ids:
            products = products.filter(category_id__in=category_ids)

        if brands_ids:
            products = products.filter(brand_id__in=brands_ids)

        if price_min:
            products = products.filter(price__gte=price_min)

        if price_max:
            products = products.filter(price__lte=price_max)

        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

        page_obj = paginatore_objects(request, products, per_page=12)

        context = {
            "products": page_obj.object_list,
            "page_obj": page_obj,
            "request": request,
            "query": query,
        }

        html_products = render_to_string("store/components/_product_list.html", context)
        html_pagination = render_to_string("store/components/_pagination.html", context)

        return JsonResponse({
            "products_html": html_products,
            "pagination_html": html_pagination,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def detail_product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    related_products = Product.objects.filter(category__name=product.category).exclude(
        name=product.name
    )[:4]
    print(related_products)
    print(product.category)
    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "store/detail_product.html", context)
