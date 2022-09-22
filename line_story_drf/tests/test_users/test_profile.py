import pytest
from rest_framework.status import HTTP_200_OK
from django.urls import reverse


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

    user.refresh_from_db()
    user.profile.refresh_from_db()
    user.profile.image.refresh_from_db()

    response = client.patch(url_profile_update)

    assert response.status_code == HTTP_200_OK
    assert response.data.get('phone') == user.profile.phone
    assert response.data.get('region') == user.profile.region
    assert response.data.get('birthday') == user.profile.birthday
    assert response.data.get('user') == user
