import pprint

from django.urls import path, include
from rest_framework import routers

from orders.views import CartViewSet, ReservationViewSet

app_name = 'orders'

cart_router = routers.DefaultRouter()
cart_router.register(r'cart', CartViewSet, basename='cart')

reserved_router = routers.DefaultRouter()
reserved_router.register(r'reserved', ReservationViewSet, basename='reserved')

pprint.pprint(cart_router.get_urls())

urlpatterns = [
    path('', include(cart_router.urls)),
    path('', include(reserved_router.urls))
]
