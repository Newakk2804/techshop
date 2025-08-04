import pytest
from accounts.models import CustomUser
from carts.models import CartItem
from store.models import Brand, Product, Category


@pytest.mark.django_db
def test_custom_user_str():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    assert str(user) == "testuser"


@pytest.mark.django_db
def test_cart_total_methods(mocker):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=100,
        discount=0,
        color="black",
        category=category,
    )
    product2 = Product.objects.create(
        name="TestProduct2",
        slug="testproduct2",
        brand=brand,
        price=50,
        discount=0,
        color="black",
        category=category,
    )
    CartItem.objects.create(user=user, product=product, quantity=2)
    CartItem.objects.create(user=user, product=product2, quantity=2)

    assert user.get_cart_total_price() == 300
    assert user.get_cart_total_quantity() == 4
