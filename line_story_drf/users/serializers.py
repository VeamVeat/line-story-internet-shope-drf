from rest_framework import serializers

from products.models import File
from users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class ImageProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ("image",)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=10)
    region = serializers.CharField(min_length=5)
    image = ImageProfileSerializer(read_only=True)
    age = serializers.IntegerField(min_value=5, max_value=120)

    class Meta:
        model = Profile
        fields = ('phone', 'region', 'image', 'age')

    def update(self, instance, validated_data):
        user_service = self.context['user_service']
        profile = user_service.update_profile()

        return profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = ImageProfileSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ('id',)


class BlockingUserSerializer(serializers.ModelSerializer):
    is_blocked = serializers.BooleanField(required=True)

    def update(self, instance, validated_data):
        user_service = self.context['user_service']
        user = user_service.blocking_user()

        return user

    class Meta:
        fields = ('is_blocked',)
        model = User





