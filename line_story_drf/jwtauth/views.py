import redis
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from users.services import UserService
from jwtauth.serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    TokenObtainMySerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailSerializer,
)
from utils.mixins import viewset_mixins

User = get_user_model()


class LoginViewSet(mixins.CreateModelMixin,
                   GenericViewSet):
    """
    Протестированно
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_response_data = {
            'email': user.email,
        }

        user_response_data.update(user.tokens)
        return Response(user_response_data, status=status.HTTP_201_CREATED)


class LogoutViewSet(mixins.UpdateModelMixin,
                    GenericViewSet):
    """
    Протестированно
    """
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RegisterUserViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """
    Протестированно
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)


# redis
class VerifyEmailViewSet(mixins.UpdateModelMixin,
                         GenericViewSet):
    serializer_class = EmailVerificationSerializer
    queryset = User.objects.all()
    lookup_field = 'token'
    permission_classes = (permissions.AllowAny,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        token = request.data.get('token')
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        user_id = r.get(token)
        user_id = int(user_id)
        instance = get_object_or_404(User, pk=user_id)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'success': 'User activated'},
                        status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class TokenObtainPairAPIView(TokenObtainPairView):
    """
    Протестированно
    """
    serializer_class = TokenObtainMySerializer


class PasswordResetViewSet(mixins.UpdateModelMixin,
                           viewset_mixins.ViewSetMixin,
                           GenericViewSet):
    serializer_class = None
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'email': ResetPasswordEmailSerializer,
        'complete': SetNewPasswordSerializer,
    }

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer(self, *args, **kwargs):
        """
        Протестированно
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        request = kwargs.get('context').get('request')

        initialization_data = {
            'request': request,
            'password': request.data.get('password')
        }

        user_service = UserService(**initialization_data)

        user_service_kwargs = {
            'user_service': user_service
        }
        kwargs['context'].update(user_service_kwargs)
        return serializer_class(*args, **kwargs)

    @action(methods=['POST'],
            detail=False)
    def email(self, request, *args, **kwargs):
        """
        отправка письма с ссылкой на активацию аккаунта (Протестированно)
        """
        email = request.data['email']

        user_service = UserService(email=email, request=request)
        response = user_service.validate_email()

        return response

    @action(methods=['post'],
            detail=False,
            url_path=r'confirm/(?P<uid64>\w+)/(?P<token>[-\w]+)',
            url_name='confirm')
    def confirm(self, request, *args, **kwargs):
        """
        Принять uid64б token -> проверить валидность ссылки для сброса пароля (Протестированно)
        """
        uid64 = kwargs.get('uid64', None)
        token = kwargs.get('token', None)

        user_service = UserService(uid64=uid64, token=token)
        user_service.check_token_to_reset_password()
        return Response({'success': 'True',
                         'uid64': uid64,
                         'token': token},
                        status=status.HTTP_200_OK)

    @action(methods=['post'],
            detail=False,
            url_path='complete/')
    def complete(self, request, *args, **kwargs):
        """
        Принять uid64, password, token -> установить новый пароль пользователю (Протестированно)
        """
        self.partial_update(request, *args, **kwargs)
        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        uid64 = request.data.get('uid64')
        user_id = force_str(urlsafe_base64_decode(uid64))
        instance = User.objects.get(id=user_id)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)
