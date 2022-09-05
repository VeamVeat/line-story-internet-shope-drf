from django.shortcuts import redirect
from django.contrib import auth
from rest_framework import mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.models import Profile
from users.serializers import (
    ProfileDetailSerializer,
    BlockingUserSerializer,
    ProfileUpdateSerializer)
from users.services import UserService
from utils.mixins.viewset_mixins import ViewSetMixin

User = auth.get_user_model()


class ProfileViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  ViewSetMixin,
                  GenericViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    serializer_class_by_action = {
        'partial_update': ProfileUpdateSerializer,
        'retrieve': ProfileDetailSerializer
    }

    def get_serializer(self, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        initial_data = dict()

        if self.action == 'partial_update':
            initial_data = {
                'age': kwargs.get('data').get('phone'),
                'phone': kwargs.get('data').get('phone'),
                'region': kwargs.get('data').get('region'),
                'image': kwargs.get('data').get('image'),
                'request': kwargs.get('context').get('request')
            }

        user_service = UserService(**initial_data)
        user_service_kwargs = {
            'user_service': user_service
        }
        kwargs['context'].update(user_service_kwargs)
        return serializer_class(*args, **kwargs)


class BlockingUserView(mixins.UpdateModelMixin,
                       ViewSetMixin,
                       GenericViewSet):

    queryset = User.objects.all()
    serializer_class = BlockingUserSerializer
    lookup_field = 'user_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'partial_update': BlockingUserSerializer,
    }

    def get_serializer(self, *args, **kwargs):
        try:
            user_email = args[0]
        except IndexError:
            user_email = ''

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        user_service = UserService(email=user_email)
        user_service_kwargs = {
            'user_service': user_service
        }
        kwargs['context'].update(user_service_kwargs)
        return serializer_class(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user_id = kwargs.get('user_id')

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return redirect('admin:users_user_change', object_id=user_id)
