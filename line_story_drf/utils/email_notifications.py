from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

import logging

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

logger = logging.getLogger(__name__)


def send_email_to_password_reset(email, request):
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(user.id)
        token = PasswordResetTokenGenerator().make_token(user)

        current_site = get_current_site(request=request).domain
        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

        absolute_url = 'http://' + current_site + relative_link
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


def send_email_to_register_user(user_data, request):
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        absolute_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.email + 'user the link below to verify your email \n' + absolute_url

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        email = EmailMessage(
                subject=data['email_subject'], body=data['email_body'], to=[data['to_email']]
        )
        email.send()
