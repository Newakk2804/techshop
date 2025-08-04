import pytest
from decimal import Decimal
from store.models import Category, Brand, Product


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    assert category.name == "Ноутбуки"
    assert category.slug == "noutbuki"
    assert str(category) == "Ноутбуки"


@pytest.mark.django_db
def test_brand_creation():
    brand = Brand.objects.create(name="Apple", slug="apple")

    assert brand.name == "Apple"
    assert brand.slug == "apple"
    assert str(brand) == "Apple"


@pytest.mark.django_db
def test_product_creation():
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    product = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        description="Мощный ноутбук для профессионалов",
        price=Decimal("2000.00"),
        discount=10,
        color="silver",
        rating=4.5,
        review_count=25,
    )

    assert product.name == "MacBook Pro"
    assert product.brand == brand
    assert product.category == category
    assert product.price == Decimal("2000.00")
    assert product.discount == 10
    assert product.color == "silver"
    assert product.rating == 4.5
    assert product.review_count == 25
    assert str(product) == "MacBook Pro"


@pytest.mark.django_db
def test_product_final_price():
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    product = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        discount=20,
        color="silver",
    )

    expected_price = Decimal("2000.00") * Decimal("0.8")
    assert product.final_price() == expected_price


@pytest.mark.django_db
def test_product_final_price_no_discount():
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    product = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        discount=0,
        color="silver",
    )

    assert product.final_price() == Decimal("2000.00")


@pytest.mark.django_db
def test_product_color_choices():
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    colors = ["black", "white", "gray", "silver", "gold"]

    for color in colors:
        product = Product.objects.create(
            name=f"Product {color}",
            slug=f"product-{color}",
            brand=brand,
            category=category,
            price=Decimal("1000.00"),
            color=color,
        )
        assert product.color == color


@pytest.mark.django_db
def test_product_meta_verbose_names():
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

    assert category._meta.verbose_name == "Категория"
    assert category._meta.verbose_name_plural == "Категории"
    assert brand._meta.verbose_name == "Бренд"
    assert brand._meta.verbose_name_plural == "Бренды"
    assert product._meta.verbose_name == "Продукт"
    assert product._meta.verbose_name_plural == "Продукты"


@pytest.mark.django_db
def test_product_relationships():
    brand = Brand.objects.create(name="Apple", slug="apple")
    category = Category.objects.create(name="Ноутбуки", slug="noutbuki")

    product1 = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        brand=brand,
        category=category,
        price=Decimal("2000.00"),
        color="silver",
    )

    product2 = Product.objects.create(
        name="MacBook Air",
        slug="macbook-air",
        brand=brand,
        category=category,
        price=Decimal("1500.00"),
        color="gold",
    )

    assert brand.products.count() == 2
    assert category.products.count() == 2
    assert product1 in brand.products.all()
    assert product2 in category.products.all()
