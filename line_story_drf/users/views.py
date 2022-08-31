from tokenize import TokenError

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from products.models import File
from users.models import Profile
from users.serializers import ProfileSerializer
from line_story_drf.settings import SIMPLE_JWT


User = auth.get_user_model()


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.phone = request.data.get("phone")
    #     instance.region = request.data.get("region")
    #     instance.save()
    #
    #     serializer = self.get_serializer(data=instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

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


class BlockedUserView(APIView):
    model = User

    def post(self, request, user_id):

        user = User.objects.get(id=user_id)
        refresh = str(RefreshToken.for_user(user))

        is_token_blacklist = BlacklistedToken.objects.filter(token__jti=refresh).exists()

        if not user.is_blocked:
            user.is_blocked = True
            user.save()

            if not is_token_blacklist:
                RefreshToken(refresh).blacklist()

        return redirect('admin:users_user_change', object_id=user_id)

