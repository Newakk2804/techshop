import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from payments.models import Payment
from orders.models import Order
from techshop.tests.create_objects_for_tests import (
    create_user,
    create_brand,
    create_category,
    create_product,
)


@pytest.mark.django_db
def test_start_payment_view_other_user_order(client):
    user1 = create_user(
        username="user1",
        email="user1@example.com",
    )
    user2 = create_user(
        username="user2",
        email="user2@example.com",
    )

    order = Order.objects.create(
        user=user1,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
    )

    client.force_login(user2)
    url = reverse("payments:start_payment", kwargs={"order_id": order.id})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_start_payment_view_paid_order(client):
    user = create_user()

    order = Order.objects.create(
        user=user,
        full_name="Иван Иванов",
        email="ivan@example.com",
        phone="+375291234567",
        address="ул. Тестовая, 1, Минск",
        paid=True,
    )

    client.force_login(user)
    url = reverse("payments:start_payment", kwargs={"order_id": order.id})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_payment_success_view_nonexistent_payment(client):
    url = reverse("payments:payment_success", kwargs={"payment_id": 99999})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_payment_cancel_view_nonexistent_payment(client):
    url = reverse("payments:payment_cancel", kwargs={"payment_id": 99999})
    response = client.get(url)

    assert response.status_code == 404
