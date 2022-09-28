import pytest
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.urls import reverse


@pytest.mark.django_db
def test_registration_user(client, user_negative_scenarios_registration_password):
    url_registration = reverse("jwtauth:register")

    response = client.post(url_registration, data=user_negative_scenarios_registration_password)
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_registration_user(client, user_negative_scenarios_registration_birthday):
    url_registration = reverse("jwtauth:register")

    response = client.post(url_registration, data=user_negative_scenarios_registration_birthday)
    assert response.status_code == HTTP_400_BAD_REQUEST
