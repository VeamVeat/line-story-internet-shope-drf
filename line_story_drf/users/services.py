import logging
from uuid import uuid4

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings

from utils.redis.services import RedisService
from utils.uid64.services import Uid64Service


class UserService:
    def __init__(self):
        self.__model = auth.get_user_model()
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def set_password(user, password):
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_profile(user, image, phone, region, age):
        user.profile.image.image = image
        user.profile.image.save()

        user.profile.phone = phone
        user.profile.region = region
        user.profile.age = age
        user.profile.save()
        return user.profile

    @staticmethod
    def check_token_to_reset_password(uid64, token):
        try:
            user = Uid64Service.get_user_by_uid64(uid64)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is isvalid', 401)

        except Exception as exp:
            raise AuthenticationFailed('The reset link is isvalid', 401)

    @staticmethod
    def __send_email_to_register_user(user, domain):
        rand_token = uuid4()

        connect_redis = RedisService()
        connect_redis.set(rand_token, user.pk)
        relative_link = reverse('email-verify')

        absolute_url = f'{settings.HTTP_SEND_EMAI}://{domain}/{relative_link}?token={rand_token}'
        email_body = f'Hi{user.email} user the link below to verify your email \n {absolute_url}'

        data = {
            'body': email_body,
            'to': user.email,
            'subject': 'Verify your email'
        }

        email_instance = EmailMessage(**data)
        email_instance.send()

    def blocking_user(self, user_id):
        user = get_object_or_404(self.__model, id=user_id)

        if user.is_blocked:
            return user

        refresh = str(RefreshToken.for_user(user))
        RefreshToken(refresh).blacklist()

        user.is_blocked = True
        user.save()
        return user

    def register_user(self, domain, email, birthday, password):
        user = self.__model(email=email, birthday=birthday, is_active=False)
        user.set_password(password)
        user.save()

        self.__send_email_to_register_user(user, domain)

        return user

    def confirm_registration(self, token):
        redis_service = RedisService()
        user_id = redis_service.get(token)

        user = get_object_or_404(self.__model, pk=user_id)
        user.is_active = True

        result = redis_service.delete(token)
        if not result:
            self.__logger.info('no such key exists')
        user.save()

        return user

    def send_email_to_password_reset(self, email, domain):
        user = get_object_or_404(self.__model, email=email)
        uid64 = Uid64Service.get_uid64_by_user_id(user.id)
        token = PasswordResetTokenGenerator().make_token(user)

        relative_link = f'password-reset-confirm/{uid64}/{token}/'

        absolute_url = f'{settings.HTTP_SEND_EMAI}://{domain}/{relative_link}'
        email_body = f'Hello {user.email}, \n user the link below to reset your password \n + {absolute_url}'

        data = {
            'body': email_body,
            'to': user.email,
            'subject': 'Reset password'
        }

        email = EmailMessage(**data)
        email.send()
