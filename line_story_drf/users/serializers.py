from rest_framework import serializers

from products.models import File
from users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UserBirthdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("birthday",)


class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("image",)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=10)
    region = serializers.CharField(min_length=5)
    image = ImageProfileSerializer(read_only=True)
    user = UserBirthdaySerializer()

    def update(self, instance, validated_data):

        request_user = self.context.get('request').user

        data_update_profile = {
            'phone': validated_data.get('phone', request_user.profile.phone),
            'region': validated_data.get('region', request_user.profile.region),
            'image': validated_data.get('image', request_user.profile.image.image),
            'birthday': validated_data.get('birthday', request_user.birthday),
            'user': self.context.get('request').user
        }

        user_service = self.context['user_service']
        profile = user_service.update_profile(**data_update_profile)

        return profile

    class Meta:
        model = Profile
        fields = ('phone', 'region', 'image', 'user', 'user')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = ImageProfileSerializer(read_only=True)

    class Meta:
        model = Profile
        exclude = ('id',)


class BlockingUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def update(self, instance, validated_data):
        user_id = validated_data.get('id')

        user_service = self.context.get('user_service')
        user = user_service.blocking_user(user_id)

        return user

    class Meta:
        model = User
        fields = ('id',)
