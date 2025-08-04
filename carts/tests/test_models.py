import pytest
from decimal import Decimal
from accounts.models import CustomUser
from carts.models import CartItem
from store.models import Brand, Category, Product


@pytest.mark.django_db
def test_cart_item_creation():
    user = CustomUser.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )
    cart_item = CartItem.objects.create(
        user=user,
        product=product,
        quantity=2,
    )

    assert cart_item.user == user
    assert cart_item.product == product
    assert cart_item.quantity == 2
    assert cart_item.added_at is not None


@pytest.mark.django_db
def test_cart_item_str_representations():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=3)

    assert str(cart_item) == "TestProduct x 3"


@pytest.mark.django_db
def test_cart_item_get_total_price():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=10,
        color="Black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=2)
    expected_price = Decimal("180.00")

    assert cart_item.get_total_price() == expected_price


@pytest.mark.django_db
def test_cart_item_get_total_price_without_discout():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")

    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("50.00"),
        discount=0,
        color="Black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=4)
    expected_price = Decimal("200.00")

    assert cart_item.get_total_price() == expected_price


@pytest.mark.django_db
def test_cart_item_unique_constraint():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    CartItem.objects.create(user=user, product=product, quantity=1)

    with pytest.raises(Exception):
        CartItem.objects.create(user=user, product=product, quantity=2)


@pytest.mark.django_db
def test_cart_item_default_quantity():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    cart_item = CartItem.objects.create(user=user, product=product)

    assert cart_item.quantity == 1
