import pytest
from rest_framework import status
from base.models import Product
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def demo_product():
    return Product.objects.create(
        user= User.objects.create_user(username="testuser", password="testpassword"),
        name="Product Name",
        price=0.00,
        brand="Sample brand",
        countInStock=0,
        category="Sample category",
        description=" "
    )

@pytest.mark.django_db
def test_get_products(client):
    url = '/api/products/'
    response = client.get(url, {'page': 1, 'keyword': 'Product'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'products' in data
    assert isinstance(data['products'], list)
    assert 'page' in data
    assert 'pages' in data

@pytest.mark.django_db
def test_get_top_products(client):
    url = '/api/products/top/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    assert all('rating' in product for product in data)


@pytest.mark.django_db
def test_update_product(client, admin_user, demo_product):
    url = f'/api/products/update/{demo_product._id}/'
    client=APIClient()
    client.force_authenticate(user=admin_user)
    data = {
        'name': 'Updated Product',
        'price': 25.0,
        'brand': 'Updated Brand',
        'countInStock': 120,
        'category': 'Updated Category',
        'description': 'Updated description'
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    updated_product = response.json()
    assert updated_product['name'] == data['name']
    assert updated_product['countInStock'] == (data['countInStock'])

@pytest.mark.django_db
def test_delete_product(client, admin_user, demo_product):
    url = f'/api/products/delete/{demo_product._id}/'
    client=APIClient()
    client.force_authenticate(user=admin_user)
    response = client.delete(url)
    assert response.status_code == 200
    assert not Product.objects.filter(_id=demo_product._id).exists()

@pytest.mark.django_db
def test_create_product_review(client, demo_product):
    url = f'/api/products/{demo_product._id}/reviews/'
    client=APIClient()
    client.force_authenticate(user= User.objects.create_user(username="testuser1", password="testpassword"))
    data = {
        'rating': 5,
        'comment': 'Great product!'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    reviews = demo_product.review_set.all()
    assert len(reviews) == 1
    assert reviews[0].rating == 5
    assert reviews[0].comment == 'Great product!'