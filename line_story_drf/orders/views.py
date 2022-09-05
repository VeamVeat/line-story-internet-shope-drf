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
from orders.services import CartItemService, ReservationService
from utils.mixins import viewset_mixins


class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewset_mixins.ViewSetMixin,
                  GenericViewSet):

    serializer_class = AddToCartSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'destroy': ChangeOfProductCartSerializer,
        'list': ProductsAllCartSerializer,
        'create': AddToCartSerializer,
        'diminish_product': ChangeOfProductCartSerializer,
        'increase_product': ChangeOfProductCartSerializer,
    }

    def get_serializer(self, *args, **kwargs):
        product_id = kwargs.get('product_id')

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        user = kwargs.get('context').get('request').user

        cart_item_services = CartItemService(
                             user=user,
                             model=CartItem,
                             product_id=product_id
        )
        product_service_kwargs = {
            'cart_item_service': cart_item_services
        }
        kwargs['context'].update(product_service_kwargs)
        return serializer_class(*args, **kwargs)

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

    @action(methods=['patch'],
            detail=False,
            url_path='diminish_product/')
    def diminish_product(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        cart_item_service = CartItemService(
                             user=request.user,
                             model=CartItem,
                             product_id=product_id
        )

        calculate_product_success = cart_item_service.diminish_product()

        if not calculate_product_success:
            return Response(
                {'error': 'Of this product in the cart  1 piece'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['patch'],
            detail=False,
            url_path='increase_product/')
    def increase_product(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        cart_item_service = CartItemService(
                            user=request.user,
                            model=CartItem,
                            product_id=product_id
        )

        calculate_product_success = cart_item_service.increase_product()
        if not calculate_product_success:
            return Response({'error': 'Product out of stock'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewset_mixins.ViewSetMixin,
                         GenericViewSet):

    serializer_class = ReservedProductSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'destroy': DeleteProductReservedSerializer,
        'list': ProductsAllCartSerializer,
        'create': ReservedProductSerializer,
    }

    def get_serializer(self, *args, **kwargs):
        product_id = kwargs.get('product_id')

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        user = kwargs.get('context').get('request').user

        reservation_services = ReservationService(
                               user=user,
                               model=CartItem,
                               product_id=product_id
        )
        product_service_kwargs = {
            'reservation_services': reservation_services
        }
        kwargs['context'].update(product_service_kwargs)
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')

        reserved_services = ReservationService(
                            user=request.user,
                            model=Reservation,
                            product_id=product_id
        )
        reserved_services.deleting_reserved_product()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewset_mixins.ViewSetMixin,
                   GenericViewSet):

    serializer_class = OrderSerializer
    lookup_field = 'product_id'
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class_by_action = {
        'list': OrderSerializer,
        'create': OrderCreateSerializer,
    }

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
