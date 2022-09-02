from django.urls import path, include
from rest_framework import routers

from orders.views import CartViewSet, ReservationViewSet

cart_router = routers.SimpleRouter()
cart_router.register(r'cart', CartViewSet, basename='cart')

reserved_router = routers.DefaultRouter()
reserved_router.register(r'reserved', ReservationViewSet, basename='reserved')

urlpatterns = [
    path('', include(cart_router.urls)),
    path('', include(reserved_router.urls))
]
