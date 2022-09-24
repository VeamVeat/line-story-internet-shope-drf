from datetime import datetime

import pytest
from rest_framework.status import HTTP_200_OK
from django.urls import reverse

from tests.settings import TEST_PHONE_USER, TEST_REGION_USER, TEST_BIRTHDAY_USER


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


def __convert_str_data_to_datatime(data):
    date_object = datetime.strptime(data, '%Y-%m-%d').date()
    return date_object


@pytest.mark.django_db
def test_profile_update(get_auth_client):
    client, user = get_auth_client

    url_profile_update = reverse(
        "users:profile-detail",
        args=[
            user.pk
        ]
    )

    date_object = __convert_str_data_to_datatime(TEST_BIRTHDAY_USER)

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
    assert __convert_str_data_to_datatime(response.data.get('birthday')) == user.birthday
