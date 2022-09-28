from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.urls import reverse

from tests.settings import TEST_QUANTITY_IN_RESERVED, TEST_QUANTITY_PRODUCT


class TestReserved:

    def test_reserved_list(self, get_client_of_reserved_product):
        client, _ = get_client_of_reserved_product

        url_cart_list = reverse("orders:reserved-list")

        response = client.get(url_cart_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1

    def test_reserved_create(self, get_auth_client, create_product):
        product = create_product
        client, _ = get_auth_client

        url_cart_create = reverse("orders:reserved-list")

        response = client.post(
            url_cart_create,
            data={
                'product_id': product.id,
                'quantity': TEST_QUANTITY_IN_RESERVED
            }
        )

        product.refresh_from_db()

        assert response.status_code == HTTP_201_CREATED
        assert response.data.get('quantity') == TEST_QUANTITY_IN_RESERVED
        assert response.data.get('product_id') == product.id

    def test_cart_destroy_product(self, get_client_of_reserved_product):
        client, reservation_product = get_client_of_reserved_product

        url_cart_create = reverse(
            "orders:reserved-detail",
            kwargs={
                'product_id': reservation_product.product.id
            }
        )

        response = client.delete(url_cart_create)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert reservation_product.product.quantity == TEST_QUANTITY_PRODUCT
