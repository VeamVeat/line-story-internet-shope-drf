from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import CartItem, Reservation, Order
from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import UserSerializer


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        cart_item_service = self.context['cart_item_service']
        user = self.context['request'].user
        cart_item = cart_item_service.add_product(user, validated_data.get('product_id'))

        return cart_item

    class Meta:
        model = CartItem
        fields = ['product_id']


class ProductsAllCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


class ChangeOfProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        product_id = attrs.get('product_id')

        is_product_exist = CartItem.objects.filter(
            user=self.context.get('request').user,
            product_id=product_id
        ).exists()

        if not is_product_exist:
            raise Http404("this product is not in the cart")
        return attrs

    class Meta:
        model = CartItem
        fields = ['product_id']


class DeleteProductReservedSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = Reservation
        fields = ['product_id']


class ReservedProductSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        quantity = attrs.get('quantity')

        product = get_object_or_404(Product, id=product_id)
        if product.quantity <= quantity:
            raise serializers.ValidationError(
                {"error": "The selected quantity exceeds the quantity in stock"}
            )
        return attrs

    def create(self, validated_data):
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity')

        reservation_service = self.context['reservation_service']

        instance = reservation_service.make_reservation(product_id, quantity)
        return instance

    class Meta:
        model = Reservation
        fields = ['product_id', 'quantity']


class ReservedAllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    count_product = serializers.IntegerField(required=True)
    address = serializers.CharField(min_length=3)

    def validate(self, attrs):
        user = self.context['request'].user

        cart_item_service = self.context['cart_item_service']
        is_user_money = cart_item_service.check_money_for_make_order(user)

        if not is_user_money:
            raise serializers.ValidationError(
                {"error": 'You don`t have enough money in your account'}
            )
        return attrs

    def create(self, validated_data):
        address = validated_data('address')

        user = self.context['request'].user
        cart_item_service = self.context['cart_item_service']
        order_service = self.context['order_service']

        all_cart_item_current_user = cart_item_service.get_all_cart_item(user)
        product_all = cart_item_service.get_products_list(all_cart_item_current_user)
        total_count = cart_item_service.get_total_product_count(all_cart_item_current_user)
        total_price = cart_item_service.get_total_price(user)

        instance = order_service.order_create(
          user,
          total_price,
          total_count,
          product_all,
          address
        )
        cart_item_service.clear(user)

        return instance

    class Meta:
        model = Reservation
        fields = ['address', 'count_product']
