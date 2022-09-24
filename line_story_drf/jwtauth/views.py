from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from line_story_drf.permissions import IsBlockedPermissions
from users.services import UserService
from jwtauth.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    TokenObtainMySerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailSerializer, VerifyEmailSerializer,
)
from utils.mixins import viewset_mixins
from utils.redis.services import RedisService

User = get_user_model()


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = auth.authenticate(
            email=serializer.data.get('email'),
            password=serializer.data.get('password')
        )

        user_response_data = {
            'email': user.email,
            **user.tokens
        }

        return Response(user_response_data, status=status.HTTP_200_OK)


class LogoutViewSet(mixins.CreateModelMixin,
                    GenericViewSet):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {'success': 'You have successfully logged out'},
            status=status.HTTP_201_CREATED
        )


class RegisterUserViewSet(mixins.CreateModelMixin,
                          viewset_mixins.MyViewSetMixin,
                          GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    serializer_class_by_action = {
        'create': RegisterSerializer
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'user_service': UserService()
        }


class VerifyEmailAPIView(mixins.UpdateModelMixin,
                         viewset_mixins.MyViewSetMixin,
                         GenericViewSet):
    queryset = User.objects.all()
    serializer_class = VerifyEmailSerializer
    permission_classes = (permissions.AllowAny,)
    serializer_class_by_action = {
        'partial_update': VerifyEmailSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'user_service': UserService()
        }

    def update(self, request, **kwargs):
        redis_service = RedisService()
        user_id = redis_service.get(request.data.get('token'))
        user = get_object_or_404(User, pk=user_id)

        serializer = self.get_serializer(user, data=request.data, partial=kwargs.get('partial'))
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            'email': user.email,
            'success': 'User activated'},
            status=status.HTTP_200_OK
        )


class TokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = TokenObtainMySerializer


class PasswordResetViewSet(mixins.UpdateModelMixin,
                           viewset_mixins.MyViewSetMixin,
                           GenericViewSet):
    serializer_class = ResetPasswordEmailSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsBlockedPermissions)

    serializer_class_by_action = {
        'email': ResetPasswordEmailSerializer,
        'complete': SetNewPasswordSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'user_service': UserService()
        }

    @action(methods=['POST'],
            detail=False)
    def email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        domain = get_current_site(request=request).domain

        user_service = self._get_service_class().get('user_service')
        user_service.send_email_to_password_reset_confirm(email, domain)

        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'],
            detail=False,
            url_path=r'confirm/(?P<uid64>\w+)/(?P<token>[-\w]+)',
            url_name='confirm')
    def confirm(self, request, *args, **kwargs):
        uid64 = kwargs.get('uid64', None)
        token = kwargs.get('token', None)

        user_service = self._get_service_class().get('user_service')
        user_service.check_token_to_reset_password(uid64, token)
        return Response(
            {'success': 'True',
             'uid64': uid64,
             'token': token},
            status=status.HTTP_200_OK
        )

    @action(methods=['PATCH'],
            detail=False)
    def complete(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )
