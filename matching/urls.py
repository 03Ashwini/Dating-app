from django.urls import path
from .views import (
    MatchListAPI,
    UserProfileAPI,
    LikeDislikeAPI,
    ProfileDetailAPI,
    FaceMatchAPIView
)

urlpatterns = [
    path('profiles/', UserProfileAPI.as_view()),
    path('profiles/<int:pk>/', ProfileDetailAPI.as_view()),
    path('like-dislike/', LikeDislikeAPI.as_view()),
    path('matches/', MatchListAPI.as_view()),
    path('face-match/', FaceMatchAPIView.as_view()),
]
