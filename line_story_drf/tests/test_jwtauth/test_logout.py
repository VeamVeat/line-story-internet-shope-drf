from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED


def test_logout_user(get_auth_client_with_refresh_token, get_data_login_user):
    url = reverse("jwtauth:logout")

    client, refresh_token = get_auth_client_with_refresh_token
    response = client.post(url, data={'token': refresh_token})

    assert response.status_code == HTTP_201_CREATED
