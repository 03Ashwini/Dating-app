from django.urls import path
from .views import (
    RegisterAPI,
    LoginAPI,
    UserAPI,
    LogoutAPI,
    RefreshTokenAPI,  # ✅ Use Custom Refresh Token API
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    # ✅ Register a new user
    path('register/', RegisterAPI.as_view(), name='register'),

    # ✅ Login user and get tokens
    path('login/', LoginAPI.as_view(), name='login'),

    # ✅ Get authenticated user data
    path('user/', UserAPI.as_view(), name='user'),

    # ✅ Logout and blacklist refresh token
    path('logout/', LogoutAPI.as_view(), name='logout'),

    # ✅ Use Custom Refresh Token API
    path('token/refresh/', RefreshTokenAPI.as_view(), name='token_refresh'),

    # ✅ Optional: Verify JWT token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
