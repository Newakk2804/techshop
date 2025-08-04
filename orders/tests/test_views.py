import pytest
from decimal import Decimal
from django.urls import reverse
from orders.models import Order, OrderItem
from carts.models import CartItem
from techshop.tests.create_objects_for_tests import (
    create_product,
    create_brand,
    create_category,
    create_user,
)


@pytest.mark.django_db
def test_order_create_view_get_authenticated_user(client):
    user = create_user()
    client.force_login(user)

    url = reverse("orders:order_create")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert "cart_items" in response.context
    assert "total_price" in response.context
    assert "total_quantity" in response.context


@pytest.mark.django_db
def test_order_create_view_get_unauthenticated_user(client):
    url = reverse("orders:order_create")
    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_order_success_view(client):
    order_id = 123

    url = reverse("orders:order_success", kwargs={"order_id": order_id})
    response = client.get(url)

    assert response.status_code == 200
    assert "order_id" in response.context
    assert response.context["order_id"] == order_id


@pytest.mark.django_db
def test_user_orders_view_authenticated_user(client):
    user = create_user()

    order1 = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order2 = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 2, Минск",
    )

    client.force_login(user)
    url = reverse("orders:user_orders")
    response = client.get(url)

    assert response.status_code == 200
    assert "orders" in response.context
    assert len(response.context["orders"]) == 2
    assert order2 in response.context["orders"]
    assert order1 in response.context["orders"]


@pytest.mark.django_db
def test_user_orders_view_unauthenticated_user(client):
    url = reverse("orders:user_orders")
    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_user_orders_view_empty_orders(client):
    user = create_user()

    client.force_login(user)
    url = reverse("orders:user_orders")
    response = client.get(url)

    assert response.status_code == 200
    assert "orders" in response.context
    assert len(response.context["orders"]) == 0


@pytest.mark.django_db
def test_user_order_detail_view_authenticated_user(client):
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    client.force_login(user)
    url = reverse("orders:user_order_detail", kwargs={"order_id": order.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "order" in response.context
    assert response.context["order"] == order


@pytest.mark.django_db
def test_user_order_detail_view_unauthenticated_user(client):
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    url = reverse("orders:user_order_detail", kwargs={"order_id": order.id})
    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_user_order_detail_view_other_user_order(client):
    """Тест доступа к заказу другого пользователя"""
    user1 = create_user(username="user1", email="user1@example.com")
    user2 = create_user(username="user2", email="user2@example.com")

    order = Order.objects.create(
        user=user1,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    client.force_login(user2)
    url = reverse("orders:user_order_detail", kwargs={"order_id": order.id})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_order_detail_view_nonexistent_order(client):
    user = create_user()

    client.force_login(user)
    url = reverse("orders:user_order_detail", kwargs={"order_id": 99999})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_order_create_view_multiple_cart_items(client):
    user = create_user()

    brand = create_brand()
    category = create_category()

    product1 = create_product(
        name="TestProduct1",
        slug="testproduct1",
        brand=brand,
        category=category,
    )

    product2 = create_product(
        name="TestProduct2",
        slug="testproduct2",
        brand=brand,
        price=Decimal("50.00"),
        discount=10,
        color="White",
        category=category,
    )

    CartItem.objects.create(user=user, product=product1, quantity=2)
    CartItem.objects.create(user=user, product=product2, quantity=1)

    client.force_login(user)
    url = reverse("orders:order_create")

    form_data = {
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+375291234567",
        "address": "ул. Тестовая, 1, Минск",
    }

    response = client.post(url, form_data)

    assert response.status_code == 302

    order = Order.objects.get(user=user)
    order_items = OrderItem.objects.filter(order=order)
    assert order_items.count() == 2

    assert not CartItem.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_order_create_view_with_product_discount(client):
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(
        brand=brand,
        discount=20,
        category=category,
    )

    CartItem.objects.create(user=user, product=product, quantity=1)

    client.force_login(user)
    url = reverse("orders:order_create")

    form_data = {
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+375291234567",
        "address": "ул. Тестовая, 1, Минск",
    }

    response = client.post(url, form_data)

    assert response.status_code == 302

    order = Order.objects.get(user=user)
    order_item = OrderItem.objects.get(order=order)
    expected_price = Decimal("100.00") * Decimal("0.8")
    assert order_item.price == expected_price
