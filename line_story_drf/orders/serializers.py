from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import CartItem, Reservation, Order
from orders.services import CartItemServices, ReservationServices, OrderServices
from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import UserSerializer


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = CartItem
        fields = ['product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']

        cart_item_services = CartItemServices(user=self.context['request'].user,
                                              model=CartItem,
                                              product_id=product_id)

        cart_item = cart_item_services.add_product()

        return cart_item


class ProductsAllCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


class ChangeOfProductCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = CartItem
        fields = ['product_id']


class DeleteProductReservedSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = Reservation
        fields = ['product_id']


class ReservedProductSerializer(serializers.ModelSerializer):
    count_product = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = Reservation
        fields = ['product_id', 'count_product']

    def validate(self, attrs):
        product_id = attrs['product_id']
        count_product = attrs['count_product']

        product = get_object_or_404(Product, id=product_id)
        if product.quantity >= count_product:
            raise serializers.ValidationError({"error": "the selected quantity exceeds the quantity in stock"})
        return attrs

    def create(self, validated_data):
        product_id = validated_data['product_id']

        reserved_services = ReservationServices(user=self.context['request'].user,
                                                model=Reservation,
                                                product_id=product_id)

        instance = reserved_services.make_reservation()

        return instance


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

    class Meta:
        model = Reservation
        fields = ['address', 'count_product']

    def validate(self, attrs):
        user = self.context['request'].user

        cart_item_services = CartItemServices(user=user, model=CartItem)
        total_price = cart_item_services.get_total_price()
        user_balance = user.wallet.ballance

        is_user_money = user_balance < total_price
        if not is_user_money:
            raise serializers.ValidationError({"error": 'You don`t have enough money in your account'})
        return attrs

    def create(self, validated_data):

        address = validated_data('address')
        user = self.context['request'].user

        cart_item_services = CartItemServices(user=user, model=CartItem)
        order_services = OrderServices(user=user, model=Reservation)

        product_all = cart_item_services.get_products_list()
        total_count = cart_item_services.get_total_product_count()
        total_price = cart_item_services.get_total_price()

        instance = order_services.order_create(total_price, total_count, product_all, address)
        cart_item_services.clear()

        return instance
