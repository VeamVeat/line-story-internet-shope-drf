import pytest
from django.urls import reverse
from rest_framework.status import HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_profile_retrieve(get_auth_blocked_client):
    client, user = get_auth_blocked_client

    url_profile_detail = reverse(
        "users:profile-detail",
        args=[
            user.pk
        ]
    )

    response = client.get(url_profile_detail)
    user.refresh_from_db()

    assert response.status_code == HTTP_403_FORBIDDEN
    assert user.is_blocked is True
