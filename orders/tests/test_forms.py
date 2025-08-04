import pytest
from orders.forms import OrderCreateForm


@pytest.mark.django_db
def test_order_create_form_valid_data():
    form_data = {
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+375291234567",
        "address": "ул. Тестовая, 1, Минск",
    }

    form = OrderCreateForm(data=form_data)

    assert form.is_valid()
    assert form.cleaned_data["full_name"] == "Иван Иванов"
    assert form.cleaned_data["email"] == "ivan@example.com"
    assert form.cleaned_data["phone"] == "+375291234567"
    assert form.cleaned_data["address"] == "ул. Тестовая, 1, Минск"


@pytest.mark.django_db
def test_order_create_form_missing_fields():
    form_data = {
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
    }

    form = OrderCreateForm(data=form_data)

    assert not form.is_valid()
    assert "phone" in form.errors
    assert "address" in form.errors


@pytest.mark.django_db
def test_order_create_form_invalid_email():
    form_data = {
        "full_name": "Иван Иванов",
        "email": "invalid-email",
        "phone": "+375291234567",
        "address": "ул. Тестовая, 1, Минск",
    }

    form = OrderCreateForm(data=form_data)

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_order_create_form_empty_fields():
    form_data = {"full_name": "", "email": "", "phone": "", "address": ""}

    form = OrderCreateForm(data=form_data)

    assert not form.is_valid()
    assert "full_name" in form.errors
    assert "email" in form.errors
    assert "phone" in form.errors
    assert "address" in form.errors


@pytest.mark.django_db
def test_order_create_form_widgets():
    form = OrderCreateForm()

    assert form.fields["full_name"].widget.attrs["class"] == "form-control"
    assert form.fields["full_name"].widget.attrs["placeholder"] == "Введите ваше ФИО"

    assert form.fields["email"].widget.attrs["class"] == "form-control"
    assert form.fields["email"].widget.attrs["placeholder"] == "Введите ваш Email"

    assert form.fields["phone"].widget.attrs["class"] == "form-control"
    assert (
        form.fields["phone"].widget.attrs["placeholder"] == "Введите ваш номер телефона"
    )

    assert form.fields["address"].widget.attrs["class"] == "form-control"
    assert (
        form.fields["address"].widget.attrs["placeholder"] == "Введите адрес доставки"
    )
    assert form.fields["address"].widget.attrs["rows"] == 3


@pytest.mark.django_db
def test_order_create_form_labels():
    form = OrderCreateForm()

    assert form.fields["full_name"].label == "ФИО"
    assert form.fields["email"].label == "Email"
    assert form.fields["phone"].label == "Номер телефона"
    assert form.fields["address"].label == "Адрес доставки"


@pytest.mark.django_db
def test_order_create_form_fields():
    form = OrderCreateForm()

    expected_fields = ["full_name", "email", "phone", "address"]
    assert list(form.fields.keys()) == expected_fields


@pytest.mark.django_db
def test_order_create_form_save():
    """Тест сохранения формы"""
    form_data = {
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
        "phone": "+375291234567",
        "address": "ул. Тестовая, 1, Минск",
    }

    form = OrderCreateForm(data=form_data)

    assert form.is_valid()

    order = form.save(commit=False)
    assert order.full_name == "Иван Иванов"
    assert order.email == "ivan@example.com"
    assert order.phone == "+375291234567"
    assert order.address == "ул. Тестовая, 1, Минск"
    assert order.status == "new"
    assert order.paid is False


@pytest.mark.django_db
def test_order_create_form_long_fields():
    long_name = "И" * 256
    long_phone = "+" + "1" * 26

    form_data = {
        "full_name": long_name,
        "email": "ivan@example.com",
        "phone": long_phone,
        "address": "ул. Тестовая, 1, Минск",
    }

    form = OrderCreateForm(data=form_data)

    assert not form.is_valid()
    assert "full_name" in form.errors
    assert "phone" in form.errors
