import pytest
import json
from decimal import Decimal
from django.urls import reverse
from favorites.models import Favorite
from techshop.tests.create_objects_for_tests import (
    create_user,
    create_brand,
    create_category,
    create_product,
)


@pytest.mark.django_db
def test_favorite_list_view_authenticated_user(client):
    user = create_user()
    client.force_login(user)
    url = reverse("favorites:list")
    response = client.get(url)

    assert response.status_code == 200
    assert "favorites" in response.context
    assert len(response.context["favorites"]) == 0


@pytest.mark.django_db
def test_favorite_list_view_unauthenticated_user(client):
    url = reverse("favorites:list")
    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_favorite_lost_view_with_items(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product1 = create_product(
        brand=brand, category=category, name="TestProduct1", slug="testproduct1"
    )
    product2 = create_product(
        brand=brand,
        category=category,
        name="TestProduct2",
        slug="testproduct2",
        price=Decimal("50.00"),
        discount=10,
        color="white",
    )
    Favorite.objects.create(user=user, product=product1)
    Favorite.objects.create(user=user, product=product2)

    client.force_login(user)
    url = reverse("favorites:list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["favorites"]) == 2
    assert product1 in [fav.product for fav in response.context["favorites"]]
    assert product2 in [fav.product for fav in response.context["favorites"]]


@pytest.mark.django_db
def test_toggle_wishlist_add_product(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)
    client.force_login(user)
    url = reverse("favorites:toggle_wishlist")
    data = {"product_id": product.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["status"] == "added"
    assert Favorite.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_toggle_wishlist_remove_product(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    Favorite.objects.create(user=user, product=product)

    client.force_login(user)
    url = reverse("favorites:toggle_wishlist")
    data = {"product_id": product.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["status"] == "removed"
    assert not Favorite.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_toggle_wishlist_unauthenticated_user(client):
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)
    url = reverse("favorites:toggle_wishlist")
    data = {"product_id": product.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_toggle_wishlist_invalid_product(client):
    user = create_user()
    client.force_login(user)
    url = reverse("favorites:toggle_wishlist")
    data = {"product_id": 99999}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Product not found"


@pytest.mark.django_db
def test_toggle_wishlist_invalid_json(client):
    user = create_user()
    client.force_login(user)
    url = reverse("favorites:toggle_wishlist")
    response = client.post(
        url,
        data="invalid json",
        content_type="application/json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_toggle_wishlist_missing_product_id(client):
    user = create_user()
    client.force_login(user)
    url = reverse("favorites:toggle_wishlist")
    data = {}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="appplication/json",
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Product not found"


@pytest.mark.django_db
def test_favorite_count_authenticated_user(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product1 = create_product(
        brand=brand,
        category=category,
        name="TestProduct1",
        slug="testproduct1",
    )
    product2 = create_product(
        brand=brand,
        category=category,
        name="TestProduct2",
        slug="testproduct2",
        price=Decimal("50.00"),
        color="White",
    )

    Favorite.objects.create(user=user, product=product1)
    Favorite.objects.create(user=user, product=product2)

    client.force_login(user)
    url = reverse("favorites:count")
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["count"] == 2


@pytest.mark.django_db
def test_favorite_count_unauthenticated_user(client):
    url = reverse("favorites:count")
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_favorite_count_empty_favorites(client):
    user = create_user()

    client.force_login(user)
    url = reverse("favorites:count")
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["count"] == 0


@pytest.mark.django_db
def test_favorite_list_view_only_user_favortes(client):
    user1 = create_user(username="user1", email="user1@example.com")
    user2 = create_user(username="user2", email="user2@example.com")
    brand = create_brand()
    category = create_category()
    product1 = create_product(
        brand=brand,
        category=category,
        name="TestProduct1",
        slug="testproduct1",
    )
    product2 = create_product(
        brand=brand,
        category=category,
        name="TestProduct2",
        slug="testproduct2",
        price=Decimal("50.00"),
        color="white",
    )

    Favorite.objects.create(user=user1, product=product1)
    Favorite.objects.create(user=user2, product=product2)

    client.force_login(user1)
    url = reverse("favorite:list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["favorites"]) == 1
    assert response.context["favorites"][0].product == product1


@pytest.mark.django_db
def test_toggle_wishlist_multiple_toggles(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    client.force_login(user)
    url = reverse("favorite:toggle_wishlist")
    data = {"product_id": product.id}

    response1 = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response1.status_code == 200
    assert response1.json()["status"] == "added"
    assert Favorite.objects.filter(user=user, product=product).exists()

    response2 = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response2.status_code == 200
    assert response2.json()["status"] == "removed"
    assert not Favorite.objects.filter(user=user, product=product).exists()

    response3 = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response3.status_code == 200
    assert response3.json()["status"] == "added"
    assert Favorite.objects.filter(user=user, product=product).exists()


@pytest.mark.django_db
def test_favorite_with_deleted_product(client):
    user = create_user()
    brand = create_brand()
    category = create_category()
    product = create_product(brand=brand, category=category)

    Favorite.objects.create(user=user, product=product)

    product.delete()

    assert not Favorite.objects.filter(user=user).exists()
