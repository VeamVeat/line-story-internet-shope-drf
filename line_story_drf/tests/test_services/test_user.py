from datetime import datetime
from uuid import uuid4

import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404

from tests.settings import TEST_NEW_PASSWORD_USER, TEST_DOMAIN
from users.models import User
from users.services import UserService
from utils.redis.services import RedisService
from utils.uid64.services import Uid64Service
from django.core import mail


class TestUserService:
    user_services = UserService()

    def test_set_password(self, get_auth_client):
        client, user_auth = get_auth_client

        user = self.user_services.set_password(user_auth, TEST_NEW_PASSWORD_USER)

        client.logout()
        is_authenticate = client.login(email=user.email, password=TEST_NEW_PASSWORD_USER)

        user.refresh_from_db()

        assert user.id == user_auth.id
        assert is_authenticate

    def test_update_profile(self, get_auth_client):
        _, user = get_auth_client

        date_object = datetime.strptime('09-19-1999', '%m-%d-%Y').date()

        data_update_profile = {
            'phone': '89525863734',
            'region': 'Республика Алтай',
            'image': user.profile.image.image,
            'birthday': date_object,
            'user': user
        }

        profile = self.user_services.update_profile(**data_update_profile)

        profile.refresh_from_db()
        user.refresh_from_db()

        assert profile.phone == data_update_profile.get('phone')
        assert profile.region == data_update_profile.get('region')
        assert user.birthday == data_update_profile.get('birthday')

    @pytest.mark.django_db
    def test_check_token_to_reset_password(self, get_auth_client):
        _, user = get_auth_client
        response = status.HTTP_200_OK

        user = get_object_or_404(User, email=user.email)
        uid64 = Uid64Service.get_uid64_by_user_id(user.id)
        token = PasswordResetTokenGenerator().make_token(user)

        try:
            self.user_services.check_token_to_reset_password(uid64, token)
        except AuthenticationFailed:
            response = status.HTTP_401_UNAUTHORIZED

        assert response == status.HTTP_200_OK

    def test_blocking_user(self, get_auth_client):
        _, user = get_auth_client

        user = self.user_services.blocking_user(user.id)

        user.refresh_from_db()

        assert user.is_blocked

    @pytest.mark.django_db
    def test_register_user(self, client, user_registration_data):
        self.user_services.register_user(
            TEST_DOMAIN,
            user_registration_data.get('email'),
            user_registration_data.get('birthday'),
            user_registration_data.get('password')
        )
        massage = mail.outbox[0].body
        assert massage

    @pytest.mark.django_db
    def test_confirm_registration(self, create_user):
        user = create_user
        user.is_active = False
        user.save()
        user.refresh_from_db()

        rand_token = uuid4()

        connect_redis = RedisService()
        connect_redis.set(rand_token, user.pk)

        user = self.user_services.confirm_registration(user, rand_token)
        user.refresh_from_db()

        assert user.is_active

    def test_send_email_to_password_reset_confirm(self, get_auth_client):
        client, user = get_auth_client

        self.user_services.send_email_to_password_reset_confirm(user.email, TEST_DOMAIN)
        massage = mail.outbox[0].body
        assert massage
