from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, RequestOTPView, VerifyOTPView


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='user-registration')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
