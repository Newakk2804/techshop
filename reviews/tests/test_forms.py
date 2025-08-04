import pytest
from decimal import Decimal
from django import forms
from reviews.forms import ReviewForm
from reviews.models import Review
from techshop.tests.create_objects_for_tests import (
    create_product,
    create_brand,
    create_category,
    create_user,
)


@pytest.mark.django_db
def test_review_form_valid_data():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    form_data = {"rating": "5", "comment": "Отличный товар!"}

    form = ReviewForm(data=form_data, user=user, product=product)

    assert form.is_valid()
    assert form.cleaned_data["rating"] == "5"
    assert form.cleaned_data["comment"] == "Отличный товар!"


@pytest.mark.django_db
def test_review_form_duplicate_review():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    Review.objects.create(
        product=product, user=user, rating=5, comment="Отличный товар!"
    )

    form_data = {"rating": "4", "comment": "Еще один отзыв"}

    form = ReviewForm(data=form_data, user=user, product=product)

    assert not form.is_valid()
    assert "Вы уже оставили отзыв для этого товара" in str(form.errors)


@pytest.mark.django_db
def test_review_form_save():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    form_data = {"rating": "5", "comment": "Отличный товар!"}

    form = ReviewForm(data=form_data, user=user, product=product)

    assert form.is_valid()

    review = form.save()

    assert review.user == user
    assert review.product == product
    assert review.rating == 5
    assert review.comment == "Отличный товар!"
    assert Review.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_review_form_widgets():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    form = ReviewForm(user=user, product=product)

    assert isinstance(form.fields["rating"].widget, forms.RadioSelect)
    assert form.fields["rating"].choices == [
        ("5", ""),
        ("4", ""),
        ("3", ""),
        ("2", ""),
        ("1", ""),
    ]

    assert form.fields["comment"].widget.attrs["class"] == "input"
    assert form.fields["comment"].widget.attrs["placeholder"] == "Ваш комментарий"
    assert form.fields["comment"].widget.attrs["rows"] == 4


@pytest.mark.django_db
def test_review_form_missing_rating():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    form_data = {"comment": "Отличный товар!"}

    form = ReviewForm(data=form_data, user=user, product=product)

    assert not form.is_valid()
    assert "rating" in form.errors
