from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from products.models import File
# from products.models import File
from users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ImageProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ("image",)


class ProfileSerializer(serializers.ModelSerializer):
    image = ImageProfileSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
