from django.urls import path, include
from rest_framework import routers

from orders.views import CartViewSet, ReservationViewSet

cart_router = routers.SimpleRouter()
cart_router.register(r'cart', CartViewSet, basename='cart')

reserved_router = routers.DefaultRouter()
reserved_router.register(r'reserved', ReservationViewSet, basename='reserved')


urlpatterns = [
    # path('add-to-cart/', CartViewSet.as_view({'post': 'create'}), name='add-to-cart'),
    # path('add-product-cart/', AddCartViewSet.as_view({'post': 'create'}), name='all-product-cart'),
    # path('all-product-cart/', ProductsCartView.as_view(), name='all-product-cart'),
    # re_path(r'delete_product_cart/(?P<product_id>[0-9]+)/$',
    #         DeleteProductCartView.as_view(), name='delete_product_cart'),


    # path('cart/', CartViewSet.as_view({'post': 'create',
    #                                    'get': 'list',
    #                                    'delete': 'destroy'}), name='user-cart'),
    # path('cart/diminish_product', CartViewSet.as_view({'path': 'diminish_product'}), name='diminish_product'),
    # path('cart/increase_product', CartViewSet.as_view({'path': 'increase_product'}), name='increase_product')

    # path('api/cart', include(router.urls))
]


urlpatterns += [
    path('', include(cart_router.urls)),
    path('', include(reserved_router.urls))
]
