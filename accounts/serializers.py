from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# ✅ Correctly using Custom User Model
User = get_user_model()


# ✅ User Serializer (For Returning User Data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# ✅ Register Serializer (For User Registration)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in response

    def create(self, validated_data):
        # ✅ Create user with encrypted password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# ✅ Login Serializer (For User Authentication)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # ✅ Allow login using either username or email
        user = User.objects.filter(username=username).first()

        # ✅ If not found, try using email to authenticate
        if user is None:
            user = User.objects.filter(email=username).first()

        # ✅ Authenticate user
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("Your account is inactive. Please contact admin.")
            return user
        else:
            raise serializers.ValidationError("Invalid username or password. Please try again!")


# ✅ Token Serializer (To Return Access & Refresh Tokens)
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


# ✅ Get Tokens for User
def get_tokens_for_user(user):
    """
    Generates JWT tokens (access and refresh) for authenticated user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
