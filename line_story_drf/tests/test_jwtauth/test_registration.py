import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from django.urls import reverse
from django.core import mail
from urllib.parse import urlparse
from urllib.parse import parse_qs


@pytest.mark.django_db
def test_registration_user(client, user_registration_data):
    url_registration = reverse("jwtauth:register")

    response = client.post(url_registration, data=user_registration_data)
    assert response.status_code == HTTP_201_CREATED

    usr_massage = mail.outbox[0].body
    parsed = urlparse(usr_massage)
    token = parse_qs(parsed.query)['token'][0]

    usl_email_verify = reverse('jwtauth:email_verify')
    response = client.patch(usl_email_verify, data={'token': token})

    assert response.status_code == HTTP_200_OK
    assert response.data.get('birthday') == user_registration_data.get('birthday')
    assert response.data('email') == user_registration_data.get('email')
