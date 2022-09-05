import logging
from uuid import uuid4

from django.http import Http404
from django.utils.encoding import smart_bytes, force_str
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.conf import settings

from products.models import File
from users.models import Profile
from utils.connect_redis import redis_service


class UserService:
    def __init__(self,
                 user_id=None,
                 email=None,
                 password=None,
                 image=None,
                 birthday=None,
                 request=None,
                 phone=None,
                 region=None,
                 age=None,
                 token=None,
                 uid64=None):

        self.model = auth.get_user_model()
        self.user_id = user_id
        self.email = email
        self.birthday = birthday
        self.password = password
        self.request = request
        self.token = token
        self.uid64 = uid64
        self.image = image
        self.region = region,
        self.age = age,
        self.phone = phone,
        self.logger = logging.getLogger(__name__)

    def blocking_user(self):
        user = get_object_or_404(self.model, email=self.email)
        refresh = str(RefreshToken.for_user(user))

        is_token_blacklist = BlacklistedToken.objects.filter(token__jti=refresh).exists()

        if not user.is_blocked:
            user.is_blocked = True
            user.save()

            if not is_token_blacklist:
                RefreshToken(refresh).blacklist()

        return user

    def register_user(self):
        user = self.model(email=self.email, birthday=self.birthday)
        user.set_password(self.password)
        user.is_active = False
        user.save()
        self.__send_email_to_register_user()
        return user

    def confirm_registration(self):
        """
        Протестировано
        """
        connect_redis = redis_service.get_connect()
        user_id = connect_redis.get(self.token)

        user = get_object_or_404(auth.get_user_model(), pk=int(user_id))
        user.is_active = True

        result = connect_redis.delete(self.token)
        if result != 1:
            self.logger.info('no such key exists')
        user.save()

        return user

    def set_password(self, request):
        """
        Установить новый пароль(Протестированно)
        """
        user = request.user
        user.set_password(self.password)
        user.save()
        return user

    def update_profile(self):
        """
        Протестированно
        """
        new_image_profile = get_object_or_404(File, id=self.request.user.profile.image.id)
        new_image_profile.image = self.image
        new_image_profile.save()

        profile = get_object_or_404(Profile, id=self.request.user.profile.id)
        profile.phone = self.phone
        profile.region = self.region
        profile.age = self.age
        profile.save()

        return profile

    def send_massage_reset_link(self):
        '''
        Имя метода
        '''
        self.__is_user_exist()
        self.__send_email_to_password_reset()

        response = Response({'success': 'We have sent you a link to reset your password'},
                            status=status.HTTP_200_OK)
        return response

    def check_token_to_reset_password(self):
        """
        Проверка валидности ссылки для сброса пароля
        """
        try:
            user_id = force_str(urlsafe_base64_decode(self.uid64))
            user = self.model.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, self.token):
                raise AuthenticationFailed('The reset link is isvalid', 401)

        except Exception as exp:
            raise AuthenticationFailed('The reset link is isvalid', 401)

    def __is_user_exist(self):
        is_user_exist = self.model.objects.filter(email=self.email).exists()

        if not is_user_exist:
            raise Http404('User not exists')

    def __send_email_to_password_reset(self):
        """
        Отправка письма для сброса пароля
        """
        user = get_object_or_404(self.model, email=self.email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request=self.request).domain

        relative_link = f'password-reset-confirm/{uidb64}/{token}/'

        absolute_url = settings.HTTP_SEND_EMAIL + '://' + current_site + '/' + relative_link
        email_body = 'Hello, \n user the link below to reset your password \n' + absolute_url

        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset password'
        }

        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def __send_email_to_register_user(self):
        """
        Отправка письма для активации аккаунта
        """
        user = self.model.objects.get(email=self.email)

        rand_token = str(uuid4())
        user_id = user.pk
        connect_redis = redis_service.get_connect()
        connect_redis.set(str(rand_token), str(user_id))

        current_site = get_current_site(self.request).domain
        relative_link = reverse('email-verify')

        absolute_url = settings.HTTP_SEND_EMAIL + '://' + current_site + relative_link + "?token=" + str(rand_token)
        email_body = 'Hi ' + user.email + 'user the link below to verify your email \n' + absolute_url

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]
        )
        email.send()
