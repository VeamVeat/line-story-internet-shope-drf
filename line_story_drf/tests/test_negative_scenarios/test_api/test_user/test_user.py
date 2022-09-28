import pytest
from django.urls import reverse
from rest_framework.status import HTTP_403_FORBIDDEN


def test_blocking_user(client, create_user):
    user = create_user

    url_blocking_user = reverse(
        "admin:blocking_user",
        kwargs={
            'id': user.id
        }
    )

    client.post(url_blocking_user)
    user.refresh_from_db()

    assert user.is_blocked is False
    assert isinstance(user.is_blocked, bool)
