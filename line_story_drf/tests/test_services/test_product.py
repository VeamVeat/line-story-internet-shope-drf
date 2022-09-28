import pytest

from products.services import ProductServices
from tests.settings import TEST_QUANTITY_PRODUCTS_IN_CART, TEST_ALL_PHOTO_PRODUCT_BY_ID


class TestProductServices:

    __product_service = ProductServices()

    def test_get_all_product_id_in_cart(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        products = self.__product_service.get_all_product_id_in_cart(cart_item.user)

        assert len(products) == TEST_QUANTITY_PRODUCTS_IN_CART

    @pytest.mark.django_db
    def test_get_all_product_photo(self, create_product):
        product = create_product

        all_photo_product = self.__product_service.get_all_product_photo(product.id)

        assert all_photo_product.count() == TEST_ALL_PHOTO_PRODUCT_BY_ID
