from django.urls import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED
from tests.settings import TEST_EMAIL_USER


def test_reset_password_email(client):
    url_password_reset_email = reverse("jwtauth:password-reset-email")

    response = client.post(
        url_password_reset_email,
        data={
            'email': TEST_EMAIL_USER
        }
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED

