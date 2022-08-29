from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = auth.get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='Confirm password')
    birthday = serializers.DateField(required=True, style={'input_type': 'date'})

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        dob = attrs['birthday']
        today = now()
        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValidationError('Must be at least 18 years old to register')

        data = super(RegisterSerializer, self).validate(attrs)
        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        birthday = validated_data['birthday']

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        if password != password2:
            raise serializers.ValidationError({'password': 'The two passwords differ.'})

        user = User(email=email, birthday=birthday)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        field = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

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

        return {
            'email': user.email,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.token = None
        self.default_error_messages = {
            'bad_token': ('Token is expired or invalid',)
        }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class TokenObtainMySerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs[self.username_field]

        user = User.objects.get(email=email)
        is_blocked = user.is_blocked

        if is_blocked:
            raise AuthenticationFailed('Your account is blocked')

        data = super().validate(attrs)
        return data


class ResetPasswordEmailRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=68, min_length=1, write_only=True)
    uidb64 = serializers.CharField(max_length=68, min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is isvalid', 401)

            user.set_password(password)
            user.save()
        except Exception as exp:
            raise AuthenticationFailed('The reset link is isvalid', 401)
        return super(SetNewPasswordSerializer, self).validate(attrs)
