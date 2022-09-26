import pytest
from rest_framework.status import HTTP_200_OK
from django.urls import reverse

from tests.settings import TEST_PHONE_USER, TEST_REGION_USER, TEST_BIRTHDAY_USER
from tests.utils.converter import convert_str_data_to_date


@pytest.mark.django_db
def test_profile_retrieve(get_auth_client):
    client, user = get_auth_client

    url_profile_detail = reverse(
        "users:profile-detail",
        args=[
            user.pk
        ]
    )

    response = client.get(url_profile_detail)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_profile_update(get_auth_client):
    client, user = get_auth_client

    url_profile_update = reverse(
        "users:profile-detail",
        args=[
            user.pk
        ]
    )

    date_object = convert_str_data_to_date(TEST_BIRTHDAY_USER)

    response = client.patch(
        url_profile_update,
        data={
            'phone': TEST_PHONE_USER,
            'region': TEST_REGION_USER,
            'birthday': date_object,
        }
    )
    user.refresh_from_db()
    user.profile.refresh_from_db()

    assert response.status_code == HTTP_200_OK
    assert response.data.get('phone') == user.profile.phone
    assert response.data.get('region') == user.profile.region
    assert convert_str_data_to_date(response.data.get('birthday')) == user.birthday
