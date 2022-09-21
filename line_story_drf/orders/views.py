from rest_framework import permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.models import CartItem, Reservation, Order
from orders.serializers import (
    AddToCartSerializer,
    ProductsAllCartSerializer,
    ChangeOfProductCartSerializer,
    ReservedProductSerializer,
    DeleteProductReservedSerializer,
    OrderSerializer,
    OrderCreateSerializer
)
from orders.services import CartItemService, ReservationService, OrderService
from utils.mixins import viewset_mixins


class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewset_mixins.MyViewSetMixin,
                  GenericViewSet):
    serializer_class = AddToCartSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'list': ProductsAllCartSerializer,
        'create': AddToCartSerializer,
        'diminish_product': ChangeOfProductCartSerializer,
        'increase_product': ChangeOfProductCartSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'cart_item_service': CartItemService()
        }

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')

        instance = get_object_or_404(
            CartItem,
            user=request.user,
            product_id=product_id
        )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'],
            detail=False,
            url_path='diminish_product/')
    def diminish_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.data.get('product_id')

        cart_item_service = self._get_service_class().get('cart_item_service')
        calculate_product_success = cart_item_service.diminish_product(request.user, product_id)

        if not calculate_product_success:
            return Response(
                {'error': 'Of this product in the cart  1 piece'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'],
            detail=False,
            url_path='increase_product/')
    def increase_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.data.get('product_id')

        cart_item_service = self._get_service_class().get('cart_item_service')
        calculate_product_success = cart_item_service.diminish_product(request.user, product_id)

        if not calculate_product_success:
            return Response(
                {'error': 'Product out of stock'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewset_mixins.MyViewSetMixin,
                         GenericViewSet):
    serializer_class = ReservedProductSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'destroy': DeleteProductReservedSerializer,
        'list': ProductsAllCartSerializer,
        'create': ReservedProductSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'reservation_service': ReservationService(user=user)
        }

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')

        reserved_service = self._get_service_class(user=request.user).get('reservation_service')
        reserved_service.deleting_reserved_product(product_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewset_mixins.MyViewSetMixin,
                   GenericViewSet):
    serializer_class = OrderSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'list': OrderSerializer,
        'create': OrderCreateSerializer,
    }

    @staticmethod
    def _get_service_class(user=None):
        return {
            'order_service': OrderService()
        }

    def get_serializer_context(self):
        context = super().get_serializer_context()

        cart_item_service = CartItemService()
        context.update({'cart_item_service': cart_item_service})
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
