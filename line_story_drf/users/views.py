from django.shortcuts import redirect
from django.contrib import auth
from rest_framework import mixins, permissions
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from products.models import File
from users.models import Profile
from users.serializers import ProfileSerializer, BlockingUserSerializer
from users.services import UserService
from utils.mixins.viewset_mixins import ViewSetMixin

User = auth.get_user_model()


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        image_data = request.FILES.get("image")
        phone = kwargs.get("phone", request.user.profile.phone)
        region = kwargs.get("region", request.user.profile.region)

        new_image_profile = get_object_or_404(File, id=request.user.profile.image.id)
        new_image_profile.image = image_data
        new_image_profile.save()

        profile = get_object_or_404(Profile, id=request.user.profile.id)
        profile.phone = phone
        profile.region = region
        profile.save()


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
