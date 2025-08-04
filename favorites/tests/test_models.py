import pytest
from favorites.models import Favorite
from techshop.tests.create_objects_for_tests import (
    create_user,
    create_brand,
    create_category,
    create_product,
)


@pytest.mark.django_db
def test_favorite_creation():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)
    favorite = Favorite.objects.create(user=user, product=product)

    assert favorite.user == user
    assert favorite.product == product
    assert favorite.added_at is not None


@pytest.mark.django_db
def test_favorite_unique_constraint():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    Favorite.objects.create(user=user, product=product)

    with pytest.raises(Exception):
        Favorite.objects.create(user=user, product=product)


@pytest.mark.django_db
def test_favorite_str_representation():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)
    favorite = Favorite.objects.create(user=user, product=product)

    expected_str = f"{user.username} - {product.name}"
    assert str(favorite) == expected_str


@pytest.mark.django_db
def test_favorite_cascade_delete_user():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    favorite = Favorite.objects.create(user=user, product=product)

    user.delete()

    assert not Favorite.objects.filter(id=favorite.id).exists()


@pytest.mark.django_db
def test_favorite_cascade_delete_product():
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    favorite = Favorite.objects.create(user=user, product=product)

    product.delete()

    assert not Favorite.objects.filter(id=favorite.id).exists()
