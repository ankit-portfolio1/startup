from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
    
    # OTP
    path('otp/generate/', views.GenerateOTPView.as_view(), name='generate_otp'),
    path('otp/verify/', views.VerifyOTPView.as_view(), name='verify_otp'),
    
    # Password
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/', views.ResetPasswordView.as_view(), name='reset_password'),
    
    # Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]