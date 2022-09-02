from rest_framework import serializers

from products.models import Product, ProductType
from users.serializers import UserSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    type = TypeSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
