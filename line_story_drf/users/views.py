from django.shortcuts import redirect
from django.contrib import auth
from rest_framework import mixins, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from line_story_drf.permissions import IsBlockedPermissions
from users.models import Profile
from users.permissions import IsNotCurrentUserPermissions
from users.serializers import (
    ProfileDetailSerializer,
    BlockingUserSerializer,
    ProfileUpdateSerializer
)
from users.services import UserService
from utils.mixins import viewset_mixins

User = auth.get_user_model()


class ProfileViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewset_mixins.MyViewSetMixin,
                     GenericViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'pk'
    http_method_names = ['get', 'patch']
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated, IsBlockedPermissions)

    serializer_class_by_action = {
        'partial_update': ProfileUpdateSerializer,
        'detail': ProfileDetailSerializer
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'user_service': UserService()
        }

    def get_object(self):
        return self.request.user.profile


class BlockingUserView(mixins.UpdateModelMixin,
                       viewset_mixins.MyViewSetMixin,
                       GenericViewSet):
    queryset = User.objects.all()
    serializer_class = BlockingUserSerializer
    lookup_field = 'id'
    permission_classes = IsNotCurrentUserPermissions

    serializer_class_by_action = {
        'update': BlockingUserSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'user_service': UserService()
        }

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser, IsNotCurrentUserPermissions]
        else:
            self.permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

        return super(BlockingUserView, self).get_permissions()

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('id'))
        serializer = self.get_serializer(user, data=kwargs, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data.get('id')

        return redirect('admin:users_user_change', object_id=user_id)
