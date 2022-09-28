import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_token_obtain_pair(get_auth_client_with_refresh_token):
    url = reverse("jwtauth:token_refresh")
    client, refresh_token = get_auth_client_with_refresh_token

    response = client.post(url, data={'refresh': refresh_token})
    assert response.status_code == HTTP_200_OK
