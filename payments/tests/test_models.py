import pytest
from decimal import Decimal
from django.utils import timezone
from payments.models import Payment
from orders.models import Order
from techshop.tests.create_objects_for_tests import (
    create_product,
    create_brand,
    create_category,
    create_user,
)


@pytest.mark.django_db
def test_payment_creation():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order,
        amount=Decimal("100.00"),
        currency="BYN",
        payment_method="paypal",
        status="pending",
        payment_id="PAY-123456789",
        transaction_id="TXN-123456789",
    )

    assert payment.order == order
    assert payment.amount == Decimal("100.00")
    assert payment.currency == "BYN"
    assert payment.payment_method == "paypal"
    assert payment.status == "pending"
    assert payment.payment_id == "PAY-123456789"
    assert payment.transaction_id == "TXN-123456789"
    assert payment.created_at is not None
    assert payment.updated_at is not None
    assert payment.paid_at is None


@pytest.mark.django_db
def test_payment_str_representation():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    expected_str = f"Платеж #{payment.id} для заказа #{order.id}"
    assert str(payment) == expected_str


@pytest.mark.django_db
def test_payment_status_choices():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    statuses = ["pending", "completed", "failed", "cancelled"]

    for status in statuses:
        payment = Payment.objects.create(
            order=order,
            amount=Decimal("100.00"),
            currency="BYN",
            payment_method="paypal",
            status=status,
        )
        assert payment.status == status


@pytest.mark.django_db
def test_payment_method_choices():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    methods = ["paypal", "card", "cash"]

    for method in methods:
        payment = Payment.objects.create(
            order=order, amount=Decimal("100.00"), currency="BYN", payment_method=method
        )
        assert payment.payment_method == method


@pytest.mark.django_db
def test_payment_default_values():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), payment_method="paypal"
    )

    assert payment.currency == "BYN"
    assert payment.status == "pending"
    assert payment.payment_id is None
    assert payment.transaction_id is None
    assert payment.paid_at is None


@pytest.mark.django_db
def test_payment_mark_as_paid():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order,
        amount=Decimal("100.00"),
        currency="BYN",
        payment_method="paypal",
        payment_id="PAY-123456789",
    )

    assert payment.status == "pending"
    assert payment.paid_at is None
    assert order.paid is False
    assert order.payment_id is None

    payment.mark_as_paid()

    payment.refresh_from_db()
    order.refresh_from_db()

    assert payment.status == "completed"
    assert payment.paid_at is not None
    assert order.paid is True
    assert order.payment_id == "PAY-123456789"


@pytest.mark.django_db
def test_payment_mark_as_failed():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    assert payment.status == "pending"

    payment.mark_as_failed()

    payment.refresh_from_db()

    assert payment.status == "failed"


@pytest.mark.django_db
def test_payment_mark_as_cancelled():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    assert payment.status == "pending"

    payment.mark_as_cancelled()

    payment.refresh_from_db()

    assert payment.status == "cancelled"


@pytest.mark.django_db
def test_payment_meta_verbose_names():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    assert payment._meta.verbose_name == "Платеж"
    assert payment._meta.verbose_name_plural == "Платежи"


@pytest.mark.django_db
def test_payment_ordering():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment1 = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    payment2 = Payment.objects.create(
        order=order, amount=Decimal("200.00"), currency="BYN", payment_method="card"
    )

    payments = Payment.objects.all()
    assert payments[0] == payment2
    assert payments[1] == payment1


@pytest.mark.django_db
def test_payment_cascade_delete():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("100.00"), currency="BYN", payment_method="paypal"
    )

    order.delete()

    assert not Payment.objects.filter(id=payment.id).exists()


@pytest.mark.django_db
def test_payment_with_different_currencies():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    currencies = ["BYN", "USD", "EUR", "RUB"]

    for currency in currencies:
        payment = Payment.objects.create(
            order=order,
            amount=Decimal("100.00"),
            currency=currency,
            payment_method="paypal",
        )
        assert payment.currency == currency


@pytest.mark.django_db
def test_payment_decimal_precision():
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    payment = Payment.objects.create(
        order=order, amount=Decimal("99.99"), currency="BYN", payment_method="paypal"
    )

    assert payment.amount == Decimal("99.99")
    assert str(payment.amount) == "99.99"
