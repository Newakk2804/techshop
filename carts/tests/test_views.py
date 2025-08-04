from this import d
import pytest
import json
from decimal import Decimal
from django.urls import reverse
from carts.models import CartItem
from store.models import Brand, Category, Product
from accounts.models import CustomUser
import time


@pytest.mark.django_db
def test_cart_view_authenticated_user(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:cart")
    response = client.get(url)

    assert response.status_code == 200
    assert "cart_items" in response.context
    assert "total_price" in response.context
    assert "total_quantity" in response.context


@pytest.mark.django_db
def test_cart_view_unauthenticated_user(client):
    url = reverse("cart:cart")
    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_cart_view_with_items(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product1 = Product.objects.create(
        name="TestProduct1",
        slug="testproduct1",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    product2 = Product.objects.create(
        name="TestProduct2",
        slug="testproduct2",
        brand=brand,
        price=Decimal("50.00"),
        discount=10,
        color="Black",
        category=category,
    )

    CartItem.objects.create(user=user, product=product1, quantity=2)
    CartItem.objects.create(user=user, product=product2, quantity=1)

    client.force_login(user)
    url = reverse("cart:cart")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["cart_items"]) == 2
    assert response.context["total_quantity"] == 3
    assert response.context["total_price"] == Decimal("245.00")


@pytest.mark.django_db
def test_cart_view_empty_cart(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:cart")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["cart_items"]) == 0
    assert response.context["total_price"] == Decimal("0.00")
    assert response.context["total_quantity"] == 0


@pytest.mark.django_db
def test_add_to_cart_authenticated_user(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {"product_id": product.id, "quantity": 2}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    cart_item = CartItem.objects.get(user=user, product=product)

    assert cart_item.quantity == 2


@pytest.mark.django_db
def test_add_to_cart_unauthenticated_user(client):
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    url = reverse("cart:add_to_cart")
    data = {
        "product_id": product.id,
        "quantity": 1,
    }
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_add_to_cart_existing_item(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    CartItem.objects.create(user=user, product=product, quantity=1)
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {"product_id": product.id, "quantity": 3}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    cart_item = CartItem.objects.get(user=user, product=product)
    assert cart_item.quantity == 4


@pytest.mark.django_db
def test_add_to_cart_default_quantity(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {
        "product_id": product.id,
    }
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

    cart_item = CartItem.objects.get(user=user, product=product)

    assert cart_item.quantity == 1


@pytest.mark.django_db
def test_add_to_cart_invalid_product(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {"product_id": 9999, "quantity": 1}

    with pytest.raises(Product.DoesNotExist):
        client.post(url, data=json.dumps(data), content_type="application/json")


@pytest.mark.django_db
def test_add_to_cart_invalid_json(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    response = client.post(url, data="invalid json", content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_remove_from_cart_authenticated_user(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    cart_item = CartItem.objects.create(user=user, product=product, quantity=2)
    client.force_login(user)
    url = reverse("cart:remove_from_cart")
    data = {"cart_item_id": cart_item.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["success"] is True
    assert response_data["total_price"] == Decimal("0.00")
    assert response_data["total_quantity"] == 0

    assert not CartItem.objects.filter(id=cart_item.id).exists()


@pytest.mark.django_db
def test_remove_from_cart_unauthenticated_user(client):
    url = reverse("cart:remove_from_cart")
    data = {"cart_item_id": 1}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_remove_cart_other_user_item(client):
    user1 = CustomUser.objects.create_user(
        username="user1", email="user1@example.com", password="testpass123"
    )
    user2 = CustomUser.objects.create_user(
        username="user2", email="user2@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )
    cart_item = CartItem.objects.create(user=user1, product=product, quantity=1)
    client.force_login(user2)
    url = reverse("cart:remove_from_cart")
    data = {"cart_item_id": cart_item.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["error"] == "Item not found"

    assert CartItem.objects.filter(id=cart_item.id).exists()


@pytest.mark.django_db
def test_remove_from_cart_nonexistent_item(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:remove_from_cart")
    data = {"cart_item_id": 99999}
    response = client.post(url, data=json.dumps(data), content_type="application/json")

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["error"] == "Item not found"


@pytest.mark.django_db
def test_remove_form_cart_updates_totals(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testBrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product1 = Product.objects.create(
        name="TestProduct1",
        slug="testproduct1",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    product2 = Product.objects.create(
        name="TestProduct2",
        slug="testproduct2",
        brand=brand,
        price=Decimal("50.00"),
        discount=10,
        color="White",
        category=category,
    )
    cart_item1 = CartItem.objects.create(user=user, product=product1, quantity=2)
    cart_item2 = CartItem.objects.create(user=user, product=product2, quantity=1)
    client.force_login(user)
    url = reverse("cart:remove_from_cart")
    data = {"cart_item_id": cart_item1.id}
    response = client.post(
        url,
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert response_data["total_price"] == "45.00"
    assert response_data["total_quantity"] == 1


@pytest.mark.django_db
def test_cart_count_authenticated_user(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@exmaple.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product1 = Product.objects.create(
        name="TestProduct1",
        slug="testproduct1",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="Black",
        category=category,
    )
    product2 = Product.objects.create(
        name="TestProduct2",
        slug="testproduct2",
        brand=brand,
        price=Decimal("50.00"),
        discount=0,
        color="White",
        category=category,
    )
    CartItem.objects.create(user=user, product=product1, quantity=3)
    CartItem.objects.create(user=user, product=product2, quantity=2)
    client.force_login(user)
    url = reverse("cart:cart_count")
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["count"] == 5


@pytest.mark.django_db
def test_cart_count_unauthenticated_user(client):
    url = reverse("cart:cart_count")
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_count_empty_cart(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client.force_login(user)
    url = reverse("cart:cart_count")
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["count"] == 0


@pytest.mark.django_db
def test_add_to_cart_zero_quantity(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )
    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {"product_id": product.id, "quantity": 0}
    response = client.post(url, data=json.dumps(data), content_type="application/json")

    assert response.status_code == 200
    assert response.json()["success"] is True

    cart_item = CartItem.objects.get(user=user, product=product)

    assert cart_item.quantity == 1


@pytest.mark.django_db
def test_add_to_cart_negative_quantity(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )

    client.force_login(user)
    url = reverse("cart:add_to_cart")
    data = {"product_id": product.id, "quantity": -1}
    response = client.post(url, data=json.dumps(data), content_type="application/json")

    assert response.status_code == 200
    assert response.json()["success"] is True

    cart_item = CartItem.objects.get(user=user, product=product)

    assert cart_item.quantity == 1


@pytest.mark.django_db
def test_cart_item_with_deleted_product(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=2)

    product.delete()

    client.force_login(user)
    url = reverse("cart:cart")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context["cart_items"]) == 0
    assert response.context["total_price"] == Decimal("0.00")
    assert response.context["total_quantity"] == 0


@pytest.mark.django_db
def test_cart_performance_with_many_items(client):
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")

    products = []
    for i in range(100):
        product = Product.objects.create(
            name=f"TestProduct{i}",
            slug=f"testproduct{i}",
            brand=brand,
            price=Decimal("10.00"),
            discount=0,
            color="black",
            category=category,
        )
        products.append(product)
        CartItem.objects.create(user=user, product=product, quantity=1)

    client.force_login(user)
    url = reverse("cart:cart")

    start_time = time.time()
    response = client.get(url)
    end_time = time.time()

    assert response.status_code == 200
    assert len(response.context["cart_items"]) == 100
    assert response.context["total_quantity"] == 100
    assert response.context["total_price"] == Decimal("1000.00")
    assert end_time - start_time < 1.0


@pytest.mark.django_db
def test_cart_with_product_discount_changes():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=2)

    assert cart_item.get_total_price() == Decimal("200.00")

    product.discount = 20
    product.save()

    cart_item.refresh_from_db()
    assert cart_item.get_total_price() == Decimal("160.00")


@pytest.mark.django_db
def test_cart_with_product_price_changes():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    brand = Brand.objects.create(name="TestBrand", slug="testbrand")
    category = Category.objects.create(name="TestCategory", slug="testcategory")
    product = Product.objects.create(
        name="TestProduct",
        slug="testproduct",
        brand=brand,
        price=Decimal("100.00"),
        discount=0,
        color="black",
        category=category,
    )

    cart_item = CartItem.objects.create(user=user, product=product, quantity=1)

    assert cart_item.get_total_price() == Decimal("100.00")

    product.price = Decimal("150.00")
    product.save()

    cart_item.refresh_from_db()
    assert cart_item.get_total_price() == Decimal("150.00")
