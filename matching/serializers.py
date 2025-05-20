# matching/serializers.py

from rest_framework import serializers
from accounts.models import CustomUser  # or your actual User model
from .models import Match, LikeDislike

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'gender', 'age', 'profile_image']

class MatchSerializer(serializers.ModelSerializer):
    user1 = UserProfileSerializer()
    user2 = UserProfileSerializer()

    class Meta:
        model = Match
        fields = '__all__'

class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'
