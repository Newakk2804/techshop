import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from django.conf import settings
from newsletters.models import Subscriber
from newsletters.tasks import send_subscription_email, send_new_product_email_task
from techshop.tests.create_objects_for_tests import (
    create_brand,
    create_category,
    create_product,
    create_user,
)


@pytest.mark.django_db
def test_send_subscription_email_task():
    email = "test@example.com"

    with patch("newsletters.tasks.send_mail") as mock_send_mail:
        result = send_subscription_email(email)

        mock_send_mail.assert_called_once_with(
            subject="Вы успешно подписались на рассылку!",
            message="Спасибо за подписку на наши новости. Мы будем держать вас в курсе!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )


@pytest.mark.django_db
def test_send_new_product_email_task_success():
    subscriber1 = Subscriber.objects.create(email="user1@example.com")
    subscriber2 = Subscriber.objects.create(email="user2@example.com")

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    with patch("newsletters.tasks.EmailMessage") as mock_email_message:
        mock_email_instance = MagicMock()
        mock_email_message.return_value = mock_email_instance

        with patch("newsletters.tasks.settings.DOMAIN", "http://localhost:8000"):
            result = send_new_product_email_task(product.slug)

            mock_email_message.assert_called_once()
            call_args = mock_email_message.call_args

            assert call_args[1]["subject"] == f"🆕 Новый товар: {product.name}"
            assert call_args[1]["from_email"] is settings.DEFAULT_FROM_EMAIL
            assert set(call_args[1]["to"]) == {"user1@example.com", "user2@example.com"}

            mock_email_instance.send.assert_called_once()


@pytest.mark.django_db
def test_send_new_product_email_task_product_not_found():
    result = send_new_product_email_task("nonexistent-product")

    assert result is None


@pytest.mark.django_db
def test_send_new_product_email_task_no_subscribers():
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    with patch("newsletters.tasks.EmailMessage") as mock_email_message:
        result = send_new_product_email_task(product.slug)

        mock_email_message.assert_not_called()
        assert result is None


@pytest.mark.django_db
def test_send_new_product_email_task_single_subscriber():
    subscriber = Subscriber.objects.create(email="user@example.com")

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    with patch("newsletters.tasks.EmailMessage") as mock_email_message:
        mock_email_instance = MagicMock()
        mock_email_message.return_value = mock_email_instance

        with patch("newsletters.tasks.settings.DOMAIN", "http://localhost:8000"):
            result = send_new_product_email_task(product.slug)

            call_args = mock_email_message.call_args
            assert call_args[1]["to"] == ["user@example.com"]


@pytest.mark.django_db
def test_send_new_product_email_task_email_content():
    subscriber = Subscriber.objects.create(email="user@example.com")

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category, discount=10)

    with patch("newsletters.tasks.EmailMessage") as mock_email_message:
        mock_email_instance = MagicMock()
        mock_email_message.return_value = mock_email_instance

        with patch("newsletters.tasks.settings.DOMAIN", "http://localhost:8000"):
            with patch("newsletters.tasks.render_to_string") as mock_render:
                mock_render.return_value = "<html>Test email content</html>"

                result = send_new_product_email_task(product.slug)

                mock_render.assert_called_once()
                call_args = mock_render.call_args

                assert call_args[0][0] == "store/emails/new_product_email.html"
                assert call_args[0][1]["product"] == product
                assert (
                    call_args[0][1]["product_url"]
                    == f"http://localhost:8000/detail-product/{product.slug}"
                )
