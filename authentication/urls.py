from django.urls import path
from .views import *

urlpatterns = [
    path('register',RegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('verify-otp', OTPVerificationView.as_view()),
    path('resend-otp', ResendOTPVerificationView.as_view()),
    path('forgot-password', ForgotPasswordView.as_view()),
    path('users', UserListView.as_view())
]