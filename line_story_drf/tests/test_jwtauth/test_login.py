import pytest
from django.urls import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_user(client, get_data_login_user):
    url = reverse("jwtauth:login")
    response = client.post(url, data=get_data_login_user)

    assert response.status_code == HTTP_401_UNAUTHORIZED

