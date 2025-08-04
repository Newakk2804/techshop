import pytest
from decimal import Decimal
from reviews.models import Review
from techshop.tests.create_objects_for_tests import (
    create_brand,
    create_category,
    create_product,
    create_user,
)


@pytest.mark.django_db
def test_review_creation():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    review = Review.objects.create(
        product=product, user=user, rating=5, comment="Отличный товар!"
    )

    assert review.product == product
    assert review.user == user
    assert review.rating == 5
    assert review.comment == "Отличный товар!"
    assert review.created_at is not None


@pytest.mark.django_db
def test_review_str_representation():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    review = Review.objects.create(
        product=product, user=user, rating=4, comment="Хороший товар"
    )

    expected_str = f"Review by {user.username} on {product.name} (4⭐)"
    assert str(review) == expected_str


@pytest.mark.django_db
def test_review_unique_constraint():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    Review.objects.create(
        product=product, user=user, rating=5, comment="Отличный товар!"
    )

    with pytest.raises(Exception):
        Review.objects.create(
            product=product, user=user, rating=4, comment="Еще один отзыв"
        )


@pytest.mark.django_db
def test_review_cascade_delete():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    review = Review.objects.create(
        product=product, user=user, rating=5, comment="Отличный товар!"
    )

    user.delete()

    assert not Review.objects.filter(id=review.id).exists()


@pytest.mark.django_db
def test_review_meta_verbose_names():
    user = create_user()

    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    review = Review.objects.create(
        product=product, user=user, rating=5, comment="Отличный товар!"
    )

    assert review._meta.verbose_name == "Отзыв"
    assert review._meta.verbose_name_plural == "Отзывы"
