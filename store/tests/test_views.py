import pytest
from decimal import Decimal
from django.urls import reverse
from store.models import Category, Brand, Product


@pytest.mark.django_db
def test_index_view(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    for i in range(7):
        Product.objects.create(
            name=f"Product {i}",
            slug=f"product-{i}",
            brand=brand,
            category=category,
            price=Decimal("1000.00"),
            color="silver",
        )

    url = reverse("store:index")
    response = client.get(url)

    assert response.status_code == 200
    assert "new_products" in response.context
    assert len(response.context["new_products"]) == 5


@pytest.mark.django_db
def test_products_all_view(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    for i in range(3):
        Product.objects.create(
            name=f"Product {i}",
            slug=f"product-{i}",
            brand=brand,
            category=category,
            price=Decimal("1000.00"),
            color="silver",
        )

    url = reverse("store:products")
    response = client.get(url)

    assert response.status_code == 200
    assert "products" in response.context
    assert "brands" in response.context
    assert "page_obj" in response.context
    assert len(response.context["products"]) == 3


@pytest.mark.django_db
def test_products_all_view_with_category_filter(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category1 = Category.objects.create(name="Ноутбуки", slug="noutbuki")
    category2 = Category.objects.create(name="Телефоны", slug="telefony")

    Product.objects.create(
        name="Laptop",
        slug="laptop",
        brand=brand,
        category=category1,
        price=Decimal("1000.00"),
        color="silver",
    )

    Product.objects.create(
        name="Phone",
        slug="phone",
        brand=brand,
        category=category2,
        price=Decimal("500.00"),
        color="black",
    )

    url = reverse("store:products")
    response = client.get(url, {"category": category1.id})

    assert response.status_code == 200
    assert len(response.context["products"]) == 1
    assert response.context["products"][0].name == "Laptop"


@pytest.mark.django_db
def test_products_all_view_with_search(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    Product.objects.create(
        name="iPhone",
        slug="iphone",
        brand=brand,
        category=category,
        price=Decimal("1000.00"),
        color="black",
    )

    url = reverse("store:products")
    response = client.get(url, {"q": "MacBook"})

    assert response.status_code == 200
    assert len(response.context["products"]) == 1
    assert response.context["products"][0].name == "MacBook Pro"


@pytest.mark.django_db
def test_detail_product_view(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    product = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    url = reverse("store:detail_product", kwargs={"product_slug": product.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert "product" in response.context
    assert response.context["product"] == product
    assert "related_products" in response.context
    assert "reviews" in response.context
    assert "form" in response.context


@pytest.mark.django_db
def test_product_filter_ajax_view(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    url = reverse("store:product_filter_ajax")
    response = client.get(url, {"category": category.id})

    assert response.status_code == 200
    assert "products_html" in response.json()
    assert "pagination_html" in response.json()


@pytest.mark.django_db
def test_product_filter_ajax_view_with_price_filter(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    Product.objects.create(
        name="MacBook Air",
        slug="macbook-air",
        brand=brand,
        category=category,
        price=Decimal("1500.00"),
        color="gold",
    )

    url = reverse("store:product_filter_ajax")
    response = client.get(url, {"min_price": "1800", "max_price": "2100"})

    assert response.status_code == 200
    response_data = response.json()
    assert "products_html" in response_data
    assert "pagination_html" in response_data


@pytest.mark.django_db
def test_product_filter_ajax_view_with_brand_filter(client):
    brand1 = Brand.objects.create(name="Apple", slug="apple")
    brand2 = Brand.objects.create(name="Samsung", slug="samsung")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand1,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    Product.objects.create(
        name="Galaxy Book",
        slug="galaxy-book",
        brand=brand2,
        category=category,
        price=Decimal("1500.00"),
        color="black",
    )

    url = reverse("store:product_filter_ajax")
    response = client.get(url, {"brand": brand1.id})

    assert response.status_code == 200
    response_data = response.json()
    assert "products_html" in response_data
    assert "pagination_html" in response_data


@pytest.mark.django_db
def test_product_filter_ajax_view_with_search(client):
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    url = reverse("store:product_filter_ajax")
    response = client.get(url, {"q": "MacBook"})

    assert response.status_code == 200
    response_data = response.json()
    assert "products_html" in response_data
    assert "pagination_html" in response_data


@pytest.mark.django_db
def test_product_filter_ajax_view_error_handling(client):
    url = reverse("store:product_filter_ajax")

    response = client.get(url, {"min_price": "invalid"})

    assert response.status_code == 500
    assert "error" in response.json()
