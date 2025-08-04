import pytest
import re
from django.urls import reverse
from accounts.models import CustomUser
from unittest.mock import patch


@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse("accounts:register")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_register_view_post(client):
    url = reverse("accounts:register")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "testpass123",
        "password2": "testpass123",
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert CustomUser.objects.filter(email="test@example.com").exists()


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse("accounts:login")
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_login_view_post(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    url = reverse("accounts:login")
    data = {
        "username": "testuser",
        "password": "testpass123",
        "remember_me": True,
    }
    response = client.post(url, data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_view(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("accounts:logout")
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_password_reset_flow_with_celery(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="oldpassword123"
    )

    with patch("accounts.forms.send_custom_email.delay") as mock_send_email:
        url = reverse("accounts:password_reset")
        response = client.post(url, {"email": "test@example.com"})

        assert response.status_code == 302
        assert mock_send_email.called

        called_args = mock_send_email.call_args[1]

        assert called_args["subject"] == "Восстановление пароля"
        assert called_args["recipient_email"] == "test@example.com"

        match = re.search(
            r"/auth/reset/([A-Za-z0-9_\-]+)/([A-Za-z0-9\-]+)/",
            called_args["message"],
        )

        assert match, "Ссылка для сброса пароля не найдена в письме"
        uidb64, token = match.groups()

    confirm_url = reverse(
        "accounts:password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
    )
    response = client.get(confirm_url)

    assert response.status_code == 302

    response = client.post(
        confirm_url,
        {"new_password1": "newpassword123", "new_password2": "newpassword123"},
    )

    assert response.status_code == 302

    login_url = reverse("accounts:login")
    login_response = client.post(
        login_url,
        {
            "username": "testuser",
            "password": "newpassword123",
        },
    )

    assert login_response.status_code == 200
