from django.shortcuts import render
from .models import Category, Brand, Product

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by("-created_at")
    context = {"categories": categories, "new_products": products[:5]}
    return render(request, "store/index.html", context)
