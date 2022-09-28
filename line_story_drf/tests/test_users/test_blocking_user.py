from django.urls import reverse
from rest_framework.status import HTTP_302_FOUND


def test_blocking_user(get_super_user_client, create_user):
    user = create_user
    api_client, admin_user = get_super_user_client

    url_blocking_user = reverse(
        "admin:blocking_user",
        kwargs={
            'id': user.id
        }
    )

    response = api_client.post(url_blocking_user)
    user.refresh_from_db()

    assert response.status_code == HTTP_302_FOUND
    assert user.is_blocked is True
    assert isinstance(user.is_blocked, bool)
