from django.urls import reverse


def test_blocking_user(get_super_user_client, create_user):
    user = create_user
    api_client, admin_user = get_super_user_client

    url_blocking_user = reverse(
        "admin:blocking_user",
        kwargs={
            'id': user.id
        }
    )

    api_client.post(url_blocking_user)
    user.refresh_from_db()
    assert user.is_blocked
