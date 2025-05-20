from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, logout
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

# ✅ Get the Custom User Model
User = get_user_model()


# 🔥 Utility to Get JWT Tokens for a User
def get_tokens_for_user(user):
    """
    Generates JWT access and refresh tokens for the given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ✅ Register API
class RegisterAPI(generics.CreateAPIView):
    """
    API to register a new user and return access & refresh tokens.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # ✅ Save the user and get tokens
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "tokens": tokens,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Login API
class LoginAPI(generics.GenericAPIView):
    """
    API to log in user and return JWT tokens.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # ✅ Validate login data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ✅ Get authenticated user
        user = serializer.validated_data

        # ✅ Get JWT tokens for the authenticated user
        tokens = get_tokens_for_user(user)

        # ✅ Return user data and tokens
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens,
        }, status=status.HTTP_200_OK)


# ✅ Get Logged-In User API
class UserAPI(generics.RetrieveAPIView):
    """
    API to get data of the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ✅ Logout API (To Blacklist Token)
class LogoutAPI(APIView):
    """
    API to logout user and blacklist refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # ✅ Get the refresh token from request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required!"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Blacklist the token to prevent reuse
            token = RefreshToken(refresh_token)
            token.blacklist()

            # ✅ Logout the user (Optional)
            logout(request)
            request.auth = None  # Clear session/auth after logout

            return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or token expired!"}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Refresh Token API (Optional but Recommended)
class RefreshTokenAPI(APIView):
    """
    API to get a new access token using the refresh token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required!"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Create new access and refresh tokens
            token = RefreshToken(refresh_token)
            data = {
                "access": str(token.access_token),
                "refresh": str(token),
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token!"}, status=status.HTTP_400_BAD_REQUEST)
