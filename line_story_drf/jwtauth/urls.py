from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUser, VerifyEmail, LoginAPIView, LogoutAPIView, LogoutAllView, TokenObtainPairAPIView, \
    PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),

    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password-reset-email/", RequestPasswordResetEmail.as_view(), name="password-reset-email"),
    path("password-reset/<uidb64>/<token>", PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path("password-reset-complete", SetNewPasswordAPIView.as_view(), name="password-reset-complete"),

]
