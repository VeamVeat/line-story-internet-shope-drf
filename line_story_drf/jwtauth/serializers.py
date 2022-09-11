from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from utils.uid64.services import Uid64Service

User = auth.get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label=_('Confirm password')
    )
    birthday = serializers.DateField(
        required=True,
        style={'input_type': 'date'}
    )

    def validate_email(self, value):
        email = value

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        return value

    def validate_birthday(self, value):
        dob = value

        today = now()
        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValidationError('Must be at least 18 years old to register')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'password': 'The two passwords differ.'})

        return attrs

    def create(self, validated_data):
        register_data = {
            'domain': get_current_site(request=self.context.get('request')).domain,
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'birthday': validated_data.get('birthday')
        }
        user_service = self.context.get('user_service')
        user = user_service.register_user(**register_data)
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if user.is_blocked:
            raise AuthenticationFailed('Your account is blocked')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return attrs

    class Meta:
        model = User
        fields = ['email', 'password']


class LogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=6)

    def save(self, **kwargs):
        try:
            token = kwargs.get('token')
            RefreshToken(token).blacklist()
        except TokenError:
            self.fail('bad token')

    class Meta:
        model = BlacklistedToken
        fields = ['token']


class TokenObtainMySerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get(self.username_field)

        user = get_object_or_404(User, email=email)
        if user.is_blocked:
            raise AuthenticationFailed('Your account is blocked')

        return super().validate(attrs)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    def validate(self, attrs):
        email = attrs.get('email')
        is_user_exist = User.objects.filter(email=email).exists()

        if not is_user_exist:
            raise Http404('User not exists')
        return attrs


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=68, min_length=1, write_only=True)
    uid64 = serializers.CharField(max_length=68, min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uid64']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uid64 = attrs.get('uid64')

            user = Uid64Service.get_user_by_uid64(uid64)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is isvalid', 401)

        except Exception as exp:
            raise AuthenticationFailed('The reset link is isvalid', 401)
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.get('password')

        user_service = self.context['user_service']
        user = self.context.get('request').user

        instance = user_service.set_password(user, password)
        return instance
