import pytest

from tests.settings import TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM, TEST_QUANTITY_IN_RESERVED


@pytest.fixture()
def get_data_cart(get_auth_client, create_product):
    client, user = get_auth_client

    data_from_cart = {
        'user': user,
        'product': create_product,
        'quantity': TEST_QUANTITY_ONE_PRODUCT_IN_CART_ITEM
    }

    return client, data_from_cart


@pytest.fixture()
def get_data_reserved(get_auth_client, create_product):
    client, user = get_auth_client

    data_from_reservation = {
        'user': user,
        'product': create_product,
        'quantity': TEST_QUANTITY_IN_RESERVED,
        'is_reserved': True
    }

    return client, data_from_reservation
