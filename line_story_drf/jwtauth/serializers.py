from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from users.services import UserService

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

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}

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
        user_service = UserService(
            request=self.context.get('request'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            birthday=validated_data.get('birthday')
        )
        user = user_service.register_user()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

    def update(self, instance, validated_data):
        token = validated_data.get('token')
        user_service = UserService(token=token)
        instance = user_service.confirm_registration()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

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

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = auth.authenticate(email=email, password=password)
        return user


class LogoutSerializer(serializers.ModelSerializer):

    token = serializers.CharField(min_length=6)

    class Meta:
        model = BlacklistedToken
        fields = ['token']

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.token = None
        self.default_error_messages = {
            'bad_token': ('Token is expired or invalid',)
        }

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class TokenObtainMySerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get(self.username_field)

        user = User.objects.get(email=email)
        is_blocked = user.is_blocked

        if is_blocked:
            raise AuthenticationFailed('Your account is blocked')

        data = super().validate(attrs)
        return data


class ResetPasswordEmailSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=68, min_length=1, write_only=True)
    uid64 = serializers.CharField(max_length=68, min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uid64']

    def validate(self, attrs):
        '''
        Протестированно
        '''
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uid64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is isvalid', 401)

        except Exception as exp:
            raise AuthenticationFailed('The reset link is isvalid', 401)
        return attrs

    def update(self, instance, validated_data):
        user_service = self.context['user_service']
        request = self.context['request']
        instance = user_service.set_password(request)
        return instance
