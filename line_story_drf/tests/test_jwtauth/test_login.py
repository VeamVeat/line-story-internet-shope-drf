from django.urls import reverse
from rest_framework.status import HTTP_200_OK


def test_login_user(create_user, client, get_data_login_user):
    url = reverse("jwtauth:login")
    response = client.post(url, data=get_data_login_user)

    assert response.status_code == HTTP_200_OK
    assert response.data.get('email') == get_data_login_user.get('email')
