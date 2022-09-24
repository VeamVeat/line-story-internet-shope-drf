import pytest

from products.models import ProductType
from tests.settings import (
    TEST_CREATED_AT_PRODUCT,
    TEST_SLUG_PRODUCT,
    TEST_TITLE_PRODUCT,
    TEST_DESCRIPTION_PRODUCT,
    TEST_PRICE_PRODUCT,
    TEST_YEAR_PRODUCT,
    TEST_QUANTITY_PRODUCT
)


@pytest.mark.django_db
@pytest.fixture()
def get_data_product():
    type_product = ProductType.objects.create(name='colored')

    data_from_product = {
        'created_at': TEST_CREATED_AT_PRODUCT,
        'type': type_product,
        'slug': TEST_SLUG_PRODUCT,
        'title': TEST_TITLE_PRODUCT,
        'description': TEST_DESCRIPTION_PRODUCT,
        'price': TEST_PRICE_PRODUCT,
        'year': TEST_YEAR_PRODUCT,
        'quantity': TEST_QUANTITY_PRODUCT
    }

    return data_from_product
