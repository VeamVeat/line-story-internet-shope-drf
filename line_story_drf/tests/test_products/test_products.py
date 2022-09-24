import pytest
from rest_framework.status import HTTP_200_OK
from django.urls import reverse


@pytest.mark.django_db
def test_product_list(get_auth_client, create_product):
    client, user = get_auth_client

    url_product_all = reverse(
        "products:product-all"
    )

    response = client.get(url_product_all)
    number_of_products_created = len(response.data)
    assert number_of_products_created == 1


@pytest.mark.django_db
def test_product_detail(get_auth_client, create_product):
    client, _ = get_auth_client
    product = create_product

    url_product_detail = reverse(
        "products:product-detail",
        args=[
            product.pk
        ]
    )

    response = client.get(url_product_detail)

    assert response.data.get('description') == product.description
    assert response.data.get('price') == product.price
    assert response.data.get('title') == product.title
    assert response.data.get('year') == product.year
    assert response.status_code == HTTP_200_OK
