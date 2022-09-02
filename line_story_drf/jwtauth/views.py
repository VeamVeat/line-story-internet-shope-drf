from rest_framework import generics, status, permissions, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from users.services import UserService
from jwtauth.serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    TokenObtainMySerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
)

User = get_user_model()


class LoginViewSet(mixins.CreateModelMixin,
                   GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)


class LogoutViewSet(mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RegisterUserViewSet(mixins.CreateModelMixin,
                          GenericViewSet):

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer(self, *args, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        birthday = kwargs.get('birthday')

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        user_service = UserService(
                       email=email,
                       password=password,
                       birthday=birthday
        )

        user_service_kwargs = {
            'user_service': user_service
        }
        kwargs['context'].update(user_service_kwargs)
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


class VerifyEmail(mixins.UpdateModelMixin,
                  GenericViewSet):

    serializer_class = EmailVerificationSerializer

    def get_serializer(self, *args, **kwargs):
        token = kwargs.get('token')

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        request = kwargs['context'].request

        user_service = UserService(token=token, request=request)

        user_service_kwargs = {
            'user_service': user_service
        }
        kwargs['context'].update(user_service_kwargs)
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


class TokenObtainPairAPIView(TokenObtainPairView):

    serializer_class = TokenObtainMySerializer


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):

        email = request.data['email']
        is_user_exist = User.objects.filter(email=email).exists()

        if not is_user_exist:
            return Response({'error': 'User not exists'},
                            status=status.HTTP_404_NOT_FOUND)

        send_email_to_password_reset(email, request)

        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'success': True,
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token,
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'success': True,
            'message': 'Password reset success',
        }, status=status.HTTP_200_OK)
