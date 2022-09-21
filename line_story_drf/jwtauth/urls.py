import pprint
from django.urls import include
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from jwtauth.views import (
    VerifyEmailAPIView,
    LogoutViewSet,
    TokenObtainPairAPIView,
    LoginViewSet,
    RegisterUserViewSet,
    PasswordResetViewSet,
)

password_reset_router = routers.DefaultRouter()
password_reset_router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

pprint.pprint(password_reset_router.get_urls())

app_name = 'jwtauth'

urlpatterns = [
    path('login/', LoginViewSet.as_view(), name='login'),
    path('logout/', LogoutViewSet.as_view({'post': 'create'}), name='logout'),
    path('email-verify/', VerifyEmailAPIView.as_view({'patch': 'partial_update'}), name='email_verify'),
    path('register/', RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
    path('', include(password_reset_router.urls)),
    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
