import re

from django.urls import reverse
from django.core import mail
from rest_framework.status import HTTP_200_OK
from tests.settings import TEST_EMAIL_USER


def test_reset_password_email(get_auth_client):
    url_password_reset_email = reverse("jwtauth:password-reset-email")
    api_client, _ = get_auth_client

    response = api_client.post(
        url_password_reset_email,
        data={
            'email': TEST_EMAIL_USER
        }
    )

    massage = mail.outbox[0].body
    assert response.status_code == HTTP_200_OK

    url_from_message = re.search("(?P<url>http?://[^\s]+)", massage).group("url")

    uid64 = url_from_message.split('/')[8]
    token = url_from_message.split('/')[9]

    url_password_reset_confirm = reverse(
        "jwtauth:password-reset-confirm",
        kwargs={
            'uid64': uid64,
            'token': token
        }
    )

    response = api_client.get(url_password_reset_confirm)
    assert response.status_code == HTTP_200_OK
    assert response.data.get('uid64') == uid64
    assert response.data.get('token') == token

    url_password_reset_complete = reverse("jwtauth:password-reset-complete")
    new_password = 'test_test'

    response = api_client.patch(
        url_password_reset_complete,
        data={
            'password': new_password,
            'token': token,
            'uid64': uid64
        }
    )
    assert response.status_code == HTTP_200_OK
