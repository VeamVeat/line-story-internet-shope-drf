from django.urls import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_302_FOUND


def test_blocking_user(get_auth_client):
    client, user = get_auth_client

    url_blocking_user = reverse(
        "admin:blocking_user",
        kwargs={
            'id': user.id
        }
    )

    response = client.post(url_blocking_user)
    user.refresh_from_db()

    assert response.status_code == HTTP_302_FOUND
    assert user.is_blocked is False
    assert isinstance(user.is_blocked, bool)


def test_blocking_user_admin(get_super_user_client):
    api_client, admin_user = get_super_user_client

    url_blocking_user = reverse(
        "admin:blocking_user",
        kwargs={
            'id': admin_user.id
        }
    )

    response = api_client.post(url_blocking_user)
    admin_user.refresh_from_db()

    assert response.status_code == HTTP_403_FORBIDDEN
    assert admin_user.is_blocked is False
    assert isinstance(admin_user.is_blocked, bool)
