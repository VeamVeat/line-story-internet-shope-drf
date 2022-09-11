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

    def update(self, instance, validated_data):

        data_update_profile = {
            'phone': validated_data.get('phone'),
            'region': validated_data.get('region'),
            'image': validated_data.get('image'),
            'age': validated_data.get('age'),
            'user': self.context.get('request').user
        }

        user_service = self.context['user_service']
        profile = user_service.update_profile(**data_update_profile)

        return profile

    class Meta:
        model = Profile
        fields = ('phone', 'region', 'image', 'age')


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
