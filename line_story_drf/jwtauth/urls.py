from django.urls import include
import pprint
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from jwtauth.views import (
    VerifyEmailViewSet,
    LogoutViewSet,
    TokenObtainPairAPIView,
    LoginViewSet,
    RegisterUserViewSet,
    PasswordResetViewSet,
)

password_reset_router = routers.DefaultRouter()
password_reset_router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

pprint.pprint(password_reset_router.get_urls())

urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    path('logout/', LogoutViewSet.as_view({'post': 'update'}), name='logout'),

    path('register/', RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
    path('email-verify/', VerifyEmailViewSet.as_view({'patch': 'partial_update'}), name='email-verify'),

    path('', include(password_reset_router.urls)),

    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
