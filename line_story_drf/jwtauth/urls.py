from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from jwtauth.views import (
    VerifyEmail,
    LogoutViewSet,
    TokenObtainPairAPIView,
    PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    LoginViewSet,
    RegisterUserViewSet,
)

urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    path('logout/', LogoutViewSet.as_view(), name='logout'),

    path('register/', RegisterUserViewSet.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path("password-reset-email/", RequestPasswordResetEmail.as_view(), name="password-reset-email"),
    path("password-reset-confirm/<uidb64>/<token>", PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path("password-reset-complete", SetNewPasswordAPIView.as_view(), name="password-reset-complete"),

    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
