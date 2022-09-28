import pytest
import tests.fixtures
from countries.models import Country, BlacklistedCountry
from tests.helpers.walk_packages import get_package_paths_in_module
from rest_framework.generics import get_object_or_404
from rest_framework.test import APIClient

from orders.models import CartItem, Reservation
from tests.settings import TEST_EMAIL_USER, TEST_USER_BALANCE
from users.models import User
from products.models import Product


pytest_plugins = [*get_package_paths_in_module(tests.fixtures)]


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def create_user(django_user_model, get_data_login_user):
    user = django_user_model.objects.create_user(**get_data_login_user)
    user.wallet.balance = TEST_USER_BALANCE
    user.wallet.save()
    return user


@pytest.fixture()
def create_super_user(django_user_model, get_data_login_super_user):
    return django_user_model.objects.create_superuser(**get_data_login_super_user)


@pytest.mark.django_db
@pytest.fixture()
def get_super_user_client(client, create_super_user, get_data_login_super_user):
    client.login(**get_data_login_super_user)
    return client, create_super_user


@pytest.mark.django_db
@pytest.fixture()
def get_auth_client(client, create_user, get_data_login_user):
    user = get_object_or_404(User, email=TEST_EMAIL_USER)

    tokens = user.tokens
    access_token = tokens.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client, user


@pytest.mark.django_db
@pytest.fixture()
def get_auth_blocked_client(client, create_user, get_data_login_user):
    user = get_object_or_404(User, email=TEST_EMAIL_USER)
    user.is_blocked = True
    user.save()

    tokens = user.tokens
    access_token = tokens.get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client, user


@pytest.fixture()
def get_auth_client_with_refresh_token(client, create_user):
    user = get_object_or_404(User, email=TEST_EMAIL_USER)

    tokens = user.tokens
    access_token = tokens.get('access')
    refresh_token = tokens.get('refresh')

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    return client, refresh_token


@pytest.mark.django_db
@pytest.fixture()
def get_client_of_cart_item(get_data_cart):
    client, data_from_cart = get_data_cart
    cart_item = CartItem.objects.create(**data_from_cart)
    return client, cart_item


@pytest.mark.django_db
@pytest.fixture()
def get_client_of_reserved_product(get_data_reserved):
    client, data_from_reserved = get_data_reserved
    reserved_product = Reservation.objects.create(**data_from_reserved)
    return client, reserved_product


@pytest.mark.django_db
@pytest.fixture()
def create_product(get_data_product):
    return Product.objects.create(**get_data_product)


@pytest.mark.django_db
@pytest.fixture()
def add_country_in_black_list():
    object_country = get_object_or_404(Country, name="Норвегия")
    BlacklistedCountry.objects.create(country=object_country)
