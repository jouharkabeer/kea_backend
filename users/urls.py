from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/', ActivateMemberView.as_view(), name='activate-member'),
    path('login/otp/', OTPLoginView.as_view(), name='login-otp'),
    path('login/otp/verify/', OTPVerifyView.as_view(), name='verify-otp'),
    path('login/password/', PasswordLoginView.as_view(), name='login-password'),
    path('login/otpcreate/', OTPSendView.as_view(), name='login-password'),
    path('login/otpverify/', VerifyOTPview.as_view(), name='login-password'),



]
