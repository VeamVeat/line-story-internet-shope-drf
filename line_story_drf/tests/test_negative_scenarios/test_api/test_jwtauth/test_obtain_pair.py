import pytest
from django.urls import reverse
from rest_framework.status import HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_token_obtain_pair(client, get_data_login_user):
    url = reverse("jwtauth:token_obtain_pair")
    response = client.post(url, data=get_data_login_user)
    assert response.status_code == HTTP_404_NOT_FOUND
