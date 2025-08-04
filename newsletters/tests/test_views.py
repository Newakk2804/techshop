import pytest
import json
from unittest.mock import patch
from django.urls import reverse
from newsletters.models import Subscriber


@pytest.mark.django_db
def test_subscribe_view_get_method(client):
    url = reverse("newsletters:subscribe")
    response = client.get(url)

    assert response.status_code == 405
    assert response.json()["success"] is False
    assert response.json()["error"] == "Invalid request"


@pytest.mark.django_db
def test_subscribe_view_successful_subscription(client):
    email = "test@example.com"

    with patch("newsletters.views.send_subscription_email.delay") as mock_send_email:
        url = reverse("newsletters:subscribe")
        data = {"email": email}
        response = client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

        assert Subscriber.objects.filter(email=email).exists()

        mock_send_email.assert_called_once_with(email)


@pytest.mark.django_db
def test_subscribe_view_missing_email(client):
    url = reverse("newsletters:subscribe")
    data = {}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"] == "Почта обязательна"


@pytest.mark.django_db
def test_subscribe_view_empty_email(client):
    url = reverse("newsletters:subscribe")
    data = {"email": ""}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"] == "Почта обязательна"


@pytest.mark.django_db
def test_subscribe_view_duplicate_email(client):
    email = "test@example.com"

    Subscriber.objects.create(email=email)

    url = reverse("newsletters:subscribe")
    data = {"email": email}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"] == "Вы уже подписчик"

    assert Subscriber.objects.filter(email=email).count() == 1


@pytest.mark.django_db
def test_subscribe_view_invalid_json(client):
    url = reverse("newsletters:subscribe")
    response = client.post(
        url,
        data="invalid json",
        content_type="application/json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_subscribe_view_case_insensitive_duplicate(client):
    email1 = "test@example.com"
    email2 = "TEST@EXAMPLE.COM"

    Subscriber.objects.create(email=email1)

    url = reverse("newsletters:subscribe")
    data = {"email": email2}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"] == "Вы уже подписчик"


@pytest.mark.django_db
def test_subscribe_view_multiple_subscriptions(client):
    emails = [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com",
    ]

    with patch("newsletters.views.send_subscription_email.delay") as mock_send_email:
        for email in emails:
            url = reverse("newsletters:subscribe")
            data = {"email": email}
            response = client.post(
                url,
                data=json.dumps(data),
                content_type="application/json",
            )

            assert response.status_code == 200
            assert response.json()["success"] is True

        assert Subscriber.objects.count() == 3

        assert mock_send_email.call_count == 3


@pytest.mark.django_db
def test_subscribe_view_with_whitespace_email(client):
    email_with_spaces = "  test@example.com  "
    clean_email = "test@example.com"

    with patch("newsletters.views.send_subscription_email.delay") as mock_send_email:
        url = reverse("newsletters:subscribe")
        data = {"email": email_with_spaces}
        response = client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

        assert Subscriber.objects.filter(email=clean_email).exists()


@pytest.mark.django_db
def test_subscribe_view_content_type_application_json(client):
    url = reverse("newsletters:subscribe")
    data = {"email": "test@example.com"}

    response = client.post(url, data=data)

    assert response.status_code == 400
