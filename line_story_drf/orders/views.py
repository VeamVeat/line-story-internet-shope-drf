from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import filters

from orders.models import CartItem, Reservation, Order
from orders.serializers import (AddToCartSerializer,
                                ProductsAllCartSerializer,
                                ChangeOfProductCartSerializer,
                                ReservedProductSerializer,
                                DeleteProductReservedSerializer,
                                OrderSerializer,
                                OrderCreateSerializer)
from orders.services import CartItemServices, ReservationServices


class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    serializer_class = AddToCartSerializer
    lookup_field = 'product_id'
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'destroy': ChangeOfProductCartSerializer,
        'list': ProductsAllCartSerializer,
        'create': AddToCartSerializer,
        'diminish_product': ChangeOfProductCartSerializer,
        'increase_product': ChangeOfProductCartSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class)

        return super(CartViewSet, self).get_serializer_class()

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        instance = CartItem.objects.get(user=request.user, product_id=product_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @action(methods=['patch'],
            detail=True,
            url_path='diminish_product/')
    def diminish_product(self, request, *args, **kwargs):
        product_id = request.data['product_id']

        cart_item_services = CartItemServices(user=request.user,
                                              model=CartItem,
                                              product_id=product_id)

        calculate_product_success = cart_item_services.diminish_product()
        if not calculate_product_success:
            return Response({'error': 'Of this product in the cart  1 piece'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['patch'],
            detail=True,
            url_path='increase_product/')
    def increase_product(self, request, *args, **kwargs):
        product_id = request.data['product_id']

        cart_item_services = CartItemServices(user=request.user,
                                              model=CartItem,
                                              product_id=product_id)

        calculate_product_success = cart_item_services.increase_product()
        if not calculate_product_success:
            return Response({'error': 'Product out of stock'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):

    serializer_class = ReservedProductSerializer
    lookup_field = 'product_id'
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'destroy': DeleteProductReservedSerializer,
        'list': ProductsAllCartSerializer,
        'create': ReservedProductSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class)

        return super(ReservationViewSet, self).get_serializer_class()

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs['product_id']

        reserved_services = ReservationServices(user=request.user,
                                                model=Reservation,
                                                product_id=product_id)
        reserved_services.deleting_reserved_product()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = OrderSerializer
    lookup_field = 'product_id'
    http_method_names = ['get', 'post']
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'list': OrderSerializer,
        'create': OrderCreateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class)

        return super(OrderViewSet, self).get_serializer_class()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)
