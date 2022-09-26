from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.urls import reverse

from orders.models import CartItem
from tests.settings import TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM, TEST_QUANTITY_PRODUCT


class TestCart:

    def test_cart_item_list(self, get_client_of_cart_item):
        client, _ = get_client_of_cart_item

        url_cart_list = reverse("orders:cart-list")

        response = client.get(url_cart_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1

    def test_cart_item_create(self, get_auth_client, create_product):
        product = create_product
        client, _ = get_auth_client

        url_cart_create = reverse("orders:cart-list")

        response = client.post(
            url_cart_create,
            data={
                'product_id': product.id
            }
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.data.get('product_id') == product.id

    def test_cart_item_diminish_product(self, get_client_of_cart_item):
        client, cart_item = get_client_of_cart_item

        url_cart_create = reverse("orders:cart-diminish-product")

        response = client.post(
            url_cart_create,
            data={
                'product_id': cart_item.product.id
            }
        )
        cart_item.refresh_from_db()

        assert response.status_code == HTTP_204_NO_CONTENT
        assert cart_item.quantity == TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM - 1
        assert cart_item.product.quantity == TEST_QUANTITY_PRODUCT + 1

    def test_cart_item_increase_product(self, get_client_of_cart_item):
        client, cart_item = get_client_of_cart_item

        url_cart_create = reverse("orders:cart-increase-product")

        response = client.post(
            url_cart_create,
            data={
                'product_id': cart_item.product.id
            }
        )
        cart_item.refresh_from_db()

        assert response.status_code == HTTP_204_NO_CONTENT
        assert cart_item.quantity == TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM + 1
        assert cart_item.product.quantity == TEST_QUANTITY_PRODUCT - 1

    def test_cart_item_destroy_product(self, get_client_of_cart_item):
        client, cart_item = get_client_of_cart_item

        url_cart_create = reverse(
            "orders:cart-detail",
            kwargs={
                'product_id': cart_item.product.id
            }
        )

        response = client.delete(url_cart_create)

        is_product_in_cart_item = CartItem.objects.filter(
            user=cart_item.user,
            product_id=cart_item.product
        ).exists()

        assert response.status_code == HTTP_204_NO_CONTENT
        assert is_product_in_cart_item is False
