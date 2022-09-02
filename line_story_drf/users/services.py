import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from line_story_drf.settings import HTTP_SEND_EMAIL


class UserService:
    def __init__(self,
                 user_id=None,
                 email=None,
                 password=None,
                 birthday=None,
                 request=None,
                 token=None):

        self.model = auth.get_user_model()
        self.user_id = user_id
        self.email = email
        self.birthday = birthday
        self.password = password
        self.request = request
        self.token = token
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
        Сделать подтверждение через Redis
        :return: response_massage
        """

        token = self.request.GET.get('token')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = self.model.objects.get(id=payload['user_id'])

        user.is_active = True
        user.save()

        return user

    def password_reset(self):
        self.__send_email_to_password_reset()
        pass

    def __send_email_to_password_reset(self):
        user = self.model.objects.get(email=self.email)
        uidb64 = urlsafe_base64_encode(user.id)
        token = PasswordResetTokenGenerator().make_token(user)

        current_site = get_current_site(request=self.request).domain
        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64,
                                                                  'token': token})

        absolute_url = HTTP_SEND_EMAIL + '://' + current_site + relative_link
        email_body = 'Hello, \n user the link below to reset your password \n' + absolute_url

        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Reset password'
        }

        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]
        )
        email.send()

    def __send_email_to_register_user(self):
        user = self.model.objects.get(email=self.email)

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(self.request).domain
        relative_link = reverse('email-verify')
        # hash link -> user
        absolute_url = HTTP_SEND_EMAIL + '://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.email + 'user the link below to verify your email \n' + absolute_url

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]
        )
        email.send()
