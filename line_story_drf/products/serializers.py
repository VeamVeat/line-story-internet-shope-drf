from rest_framework import serializers

from products.models import Product, ProductType, ProductFile, File


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        exclude = ('id',)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('id',)


class ProductFileSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)

    class Meta:
        model = ProductFile
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    product_file = ProductFileSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('type', 'description', 'price', 'title', 'year', 'product_file')
