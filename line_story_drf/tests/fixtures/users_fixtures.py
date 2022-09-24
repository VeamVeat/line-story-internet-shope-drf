import pytest

from tests.settings import (
    TEST_EMAIL_USER,
    TEST_PASSWORD_USER,
    TEST_EMAIL_SUPER_USER,
    TEST_PASSWORD_SUPER_USER,
    TEST_BIRTHDAY_USER
)


@pytest.fixture()
def get_data_login_user():
    data_form_login = {
        'email': TEST_EMAIL_USER,
        'password': TEST_PASSWORD_USER
    }
    return data_form_login


@pytest.fixture()
def get_data_login_super_user():
    data_form_login_super_user = {
        'email': TEST_EMAIL_SUPER_USER,
        'password': TEST_PASSWORD_SUPER_USER
    }
    return data_form_login_super_user


@pytest.fixture()
def user_registration_data():
    data_from_registration = {
        'email': TEST_EMAIL_USER,
        'password': TEST_PASSWORD_USER,
        'password2': TEST_PASSWORD_USER,
        'birthday': TEST_BIRTHDAY_USER
    }
    return data_from_registration
