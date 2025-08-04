import pytest
from decimal import Decimal
from orders.models import Order, OrderItem
from techshop.tests.create_objects_for_tests import (
    create_product,
    create_brand,
    create_category,
    create_user,
)


@pytest.mark.django_db
def test_order_creation():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
        status="new",
        paid=False,
    )

    assert order.user == user
    assert order.full_name == "Иван Иванов"
    assert order.email == "ivan@example.com"
    assert order.phone == "+375291234567"
    assert order.address == "ул. Тестовая, 1, Минск"
    assert order.status == "new"
    assert order.paid is False
    assert order.created_at is not None
    assert order.updated_at is not None


@pytest.mark.django_db
def test_order_str_representation():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    expected_str = f"Заказ #{order.id} от Иван Иванов"
    assert str(order) == expected_str


@pytest.mark.django_db
def test_order_status_choices():
    user = create_user()

    statuses = ["new", "processing", "shipped", "completed", "canceled"]

    for status in statuses:
        order = Order.objects.create(
            user=user,
            full_name="Иван Иванов",
            email="ivan@example.com",
            phone="+375291234567",
            address="ул. Тестовая, 1, Минск",
            status=status,
        )
        assert order.status == status


@pytest.mark.django_db
def test_order_default_values():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    assert order.status == "new"
    assert order.paid is False
    assert order.payment_id is None


@pytest.mark.django_db
def test_order_without_user():
    order = Order.objects.create(
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    assert order.user is None
    assert order.full_name == "Иван Иванов"


@pytest.mark.django_db
def test_order_meta_verbose_names():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    assert order._meta.verbose_name == "Заказ"
    assert order._meta.verbose_name_plural == "Заказы"


@pytest.mark.django_db
def test_order_ordering():
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
        full_name="Петр Петров",
        email="petr@example.com",
        phone="+375291234568",
        address="ул. Тестовая, 2, Минск",
    )

    orders = Order.objects.all()
    assert orders[0] == order2
    assert orders[1] == order1


@pytest.mark.django_db
def test_orderitem_creation():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, price=Decimal("100.00"), quantity=2
    )

    assert order_item.order == order
    assert order_item.product == product
    assert order_item.price == Decimal("100.00")
    assert order_item.quantity == 2


@pytest.mark.django_db
def test_orderitem_str_representation():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, price=Decimal("100.00"), quantity=2
    )

    expected_str = f"{product.name} x 2"
    assert str(order_item) == expected_str


@pytest.mark.django_db
def test_orderitem_get_cost():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, price=Decimal("100.00"), quantity=3
    )

    expected_cost = Decimal("100.00") * 3
    assert order_item.get_cost() == expected_cost


@pytest.mark.django_db
def test_order_get_total_cost():
    user = create_user()

    brand = create_brand()
    category = create_category()

    product1 = create_product(
        brand=brand,
        category=category,
        name="TestProduct1",
        slug="testproduct1",
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

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    OrderItem.objects.create(
        order=order, product=product1, price=Decimal("100.00"), quantity=2
    )

    OrderItem.objects.create(
        order=order,
        product=product2,
        price=Decimal("45.00"),
        quantity=1,
    )

    expected_total = Decimal("100.00") * 2 + Decimal("45.00") * 1
    assert order.get_total_cost() == expected_total


@pytest.mark.django_db
def test_order_get_total_quantity():
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
        color="White",
        category=category,
    )

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    OrderItem.objects.create(
        order=order, product=product1, price=Decimal("100.00"), quantity=3
    )

    OrderItem.objects.create(
        order=order, product=product2, price=Decimal("50.00"), quantity=2
    )

    expected_quantity = 3 + 2
    assert order.get_total_quantity() == expected_quantity


@pytest.mark.django_db
def test_orderitem_meta_verbose_names():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, price=Decimal("100.00"), quantity=1
    )

    assert order_item._meta.verbose_name == "Позиция заказа"
    assert order_item._meta.verbose_name_plural == "Позиции заказа"


@pytest.mark.django_db
def test_order_cascade_delete():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, price=Decimal("100.00"), quantity=1
    )

    order.delete()

    assert not OrderItem.objects.filter(id=order_item.id).exists()
