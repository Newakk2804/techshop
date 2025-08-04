import pytest
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from accounts.models import CustomUser


@pytest.mark.django_db
def test_user_creation_form_valid():
    form = CustomUserCreationForm(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_creation_form_email_unique():
    CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    form = CustomUserCreationForm(
        data={
            "username": "testuser2",
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_authentication_form_fields():
    form = CustomAuthenticationForm()
    assert "username" in form.fields
    assert "password" in form.fields
    assert "remember_me" in form.fields
