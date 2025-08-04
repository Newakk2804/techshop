from decimal import Decimal
from store.models import Brand, Category, Product
from accounts.models import CustomUser


def create_user(username="testuser", email="test@example.com", password="testpass123"):
    return CustomUser.objects.create_user(
        username=username, email=email, password=password
    )


def create_brand():
    return Brand.objects.create(name="TestBrand", slug="testbrand")


def create_category():
    return Category.objects.create(name="TestCategory", slug="testcategory")


def create_product(
    brand,
    category,
    name="TestProduct",
    slug="testproduct",
    price=Decimal("100.00"),
    discount=0,
    color="Black",
):
    return Product.objects.create(
        name=name,
        slug=slug,
        brand=brand,
        price=price,
        discount=discount,
        color=color,
        category=category,
    )
