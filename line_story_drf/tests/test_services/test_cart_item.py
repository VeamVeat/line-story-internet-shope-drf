from decimal import Decimal

from orders.models import CartItem
from orders.services import CartItemService
from tests.settings import (
    TEST_QUANTITY_PRODUCT,
    TEST_PRICE_PRODUCT,
    TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM,
    TEST_QUANTITY_ALL_PRODUCT_IN_CART_ITEM,
    TEST_QUANTITY_PRODUCTS_IN_CART
)


class TestCartItemService:

    __cart_item_service = CartItemService()

    def __get_total_count_product_cart(self, user):
        all_cart_item_current_user = self.__cart_item_service.get_all_cart_item(user)
        return self.__cart_item_service.get_total_product_count(all_cart_item_current_user)

    def __get_products_list(self, user):
        all_cart_item_current_user = self.__cart_item_service.get_all_cart_item(user)
        return self.__cart_item_service.get_products_list(all_cart_item_current_user)

    @staticmethod
    def __is_products_in_cart_item_by_user(cart_item):
        is_product_exist = CartItem.objects.filter(user=cart_item.user, product_id=cart_item.product.id).exists()
        return is_product_exist

    @staticmethod
    def __is_products_in_cart_item(cart_item):
        is_product_exist = CartItem.objects.filter(user=cart_item.user).exists()
        return is_product_exist

    def test_get_total_product_count(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        total_count = self.__get_total_count_product_cart(cart_item.user)

        assert total_count == TEST_QUANTITY_ALL_PRODUCT_IN_CART_ITEM

    def test_get_products_list(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        products = self.__get_products_list(cart_item.user)

        assert len(products) == TEST_QUANTITY_PRODUCTS_IN_CART

    def test_check_money_for_make_order(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        is_user_money = self.__cart_item_service.check_money_for_make_order(cart_item.user)

        assert is_user_money is True

    def test_get_total_price(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        total_price_after = self.__cart_item_service.get_total_price(cart_item.user)
        total_price_before = TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM * Decimal(TEST_PRICE_PRODUCT)

        assert total_price_before == total_price_after

    def test_get_quantity_product_in_cart(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        product_quantity = self.__cart_item_service.get_quantity_product_in_cart(
            cart_item.user,
            cart_item.product.id
        )
        assert product_quantity == TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM

    def test_increase_product(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        is_increase_product = self.__cart_item_service.increase_product(
            cart_item.user,
            cart_item.product.id
        )
        cart_item.refresh_from_db()

        assert is_increase_product is True
        assert cart_item.quantity == TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM + 1
        assert cart_item.product.quantity == TEST_QUANTITY_PRODUCT - 1

    def test_diminish_product(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        is_increase_product = self.__cart_item_service.diminish_product(
            cart_item.user,
            cart_item.product.id
        )
        cart_item.refresh_from_db()

        assert is_increase_product is True
        assert cart_item.quantity == TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM - 1
        assert cart_item.product.quantity == TEST_QUANTITY_PRODUCT + 1

    def test_delete_product(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        self.__cart_item_service.delete_product(
            cart_item.user,
            cart_item.product.id
        )
        product_exist = self.__is_products_in_cart_item_by_user(cart_item)
        assert product_exist is False

    def test_add_product(self, create_user, create_product):
        user = create_user
        product = create_product

        cart_item = self.__cart_item_service.add_product(user, product.id)

        assert cart_item.product.id == product.id

    def test_clear(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        self.__cart_item_service.clear(cart_item.user)
        product_exist = self.__is_products_in_cart_item(cart_item)

        assert product_exist is False

    def test_get_all_cart_item(self, get_client_of_cart_item):
        _, cart_item = get_client_of_cart_item

        cart_item = self.__cart_item_service.get_all_cart_item(cart_item.user)

        assert cart_item.count() == 1
