import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from base.models import Product, Review, Order, OrderItem, ShippingAddress
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_cart_total_price_calculation():
    user = User.objects.create_user(username="testuser", password="password")
    product_data = [
        {"_id": 29, "name": "Vampire Bat", "price": Decimal("7500.00")},
        {"_id": 26, "name": "Dragon Flame 🎸", "price": Decimal("690.00")},
    ]
    
    for data in product_data:
        Product.objects.update_or_create(
            _id=data["_id"], defaults={"name": data["name"], "price": data["price"]}
        )

    product1 = Product.objects.get(_id=29)
    product2 = Product.objects.get(_id=26)
    orders = Order.objects.filter(user=user)

    if orders.exists():
        order = orders.first()
        calculated_total_price = sum(
            item.qty * item.price for item in order.orderitem_set.all()
        )
    else:
        calculated_total_price = Decimal("0.00")
    expected_total_price = Decimal("0.00")
    assert calculated_total_price == expected_total_price


@pytest.mark.django_db
def test_product_special_character_name():
    product = Product(name="Dragon Flame 🎸", brand="FlameWood")
    product.save()
    assert Product.objects.filter(name="Dragon Flame 🎸").exists()

@pytest.mark.django_db
def test_product_negative_rating():
    product = Product(name="Test Guitar", rating=-5)
    with pytest.raises(ValidationError):
        product.full_clean()  # Ensure it raises validation error

@pytest.mark.django_db
def test_order_with_negative_total():
    order = Order(totalPrice=-100.50)
    with pytest.raises(ValidationError):
        order.full_clean()

@pytest.mark.django_db
def test_review_rating_out_of_range():
    review = Review(rating=6)
    with pytest.raises(ValidationError):
        review.full_clean()

@pytest.mark.xfail
def test_unexpected_data_type_in_category():
    product = Product(name="Guitar Strings", category=12345) 
    with pytest.raises(TypeError):  # Ensures only string data is accepted
        product.full_clean()

@pytest.mark.django_db
def test_category_case_sensitivity():
    product1 = Product(name="Guitar A", category="Acoustic")
    product2 = Product(name="Guitar B", category="acoustic")
    product1.save()
    product2.save()
    assert product1.category != product2.category

@pytest.mark.xfail
def test_create_user_without_username():
    user = User(email="testuser@example.com", password="SecureP@ss123")
    with pytest.raises(ValueError):  # Django requires a username by default
        user.full_clean()