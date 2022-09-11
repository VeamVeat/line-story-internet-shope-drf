from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
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
    ResetPasswordEmailSerializer,
)
from utils.mixins import viewset_mixins

User = get_user_model()


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny, IsBlockedPermissions)

    def post(self, request):
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

        return Response(user_response_data, status=status.HTTP_201_CREATED)


class LogoutViewSet(mixins.UpdateModelMixin,
                    GenericViewSet):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RegisterUserViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


class VerifyEmailViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny, IsBlockedPermissions)

    def patch(self, request, *args, **kwargs):
        token = request.data.get('token')

        user_service = UserService()
        user = user_service.confirm_registration(token)

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
    serializer_class = None
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsBlockedPermissions)

    serializer_class_by_action = {
        'email': ResetPasswordEmailSerializer,
        'complete': SetNewPasswordSerializer,
    }
    service_class = {
        'user_service': UserService()
    }

    @action(methods=['POST'],
            detail=False)
    def email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        domain = get_current_site(request=request).domain

        user_service = self.service_class.get('user_service')
        user_service.send_email_to_password_reset(email, domain)

        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'],
            detail=False,
            url_path=r'confirm/(?P<uid64>\w+)/(?P<token>[-\w]+)',
            url_name='confirm')
    def confirm(self, request, *args, **kwargs):
        uid64 = kwargs.get('uid64', None)
        token = kwargs.get('token', None)

        user_service = self.service_class.get('user_service')
        user_service.check_token_to_reset_password(uid64, token)
        return Response(
            {'success': 'True',
             'uid64': uid64,
             'token': token},
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'],
            detail=False,
            url_path='complete/')
    def complete(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )
