from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, RequestOTPView, VerifyOTPView



urlpatterns = [
    path('register/', UserRegistrationViewSet.as_view(), name='user-registration'),
    path('auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
