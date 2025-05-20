from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .models import Match
from .serializers import MatchSerializer, UserProfileSerializer
from .face_matcher import face_rec_model, shape_predictor
import dlib
import os
from django.conf import settings

User = get_user_model()


class MatchListAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        matches = Match.objects.filter(user=request.user)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


class UserProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeDislikeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, target_user_id):
        try:
            target_user = User.objects.get(id=target_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")

        if action == "like":
            Match.objects.get_or_create(user=request.user, matched_user=target_user)
            return Response({"message": "User liked"})
        elif action == "dislike":
            Match.objects.filter(user=request.user, matched_user=target_user).delete()
            return Response({"message": "User disliked"})
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class FaceMatchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get("image")
        if not uploaded_file:
            return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_path = os.path.join(settings.MEDIA_ROOT, "temp_upload.jpg")
            with open(image_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            uploaded_img = dlib.load_rgb_image(image_path)
            user_img_path = request.user.profile_picture.path  # Ensure user has a `profile_picture` field

            user_img = dlib.load_rgb_image(user_img_path)

            detector = dlib.get_frontal_face_detector()
            faces1 = detector(user_img)
            faces2 = detector(uploaded_img)

            if len(faces1) == 0 or len(faces2) == 0:
                return Response({"error": "Face not detected in one or both images"}, status=400)

            shape1 = shape_predictor(user_img, faces1[0])
            shape2 = shape_predictor(uploaded_img, faces2[0])
            desc1 = face_rec_model.compute_face_descriptor(user_img, shape1)
            desc2 = face_rec_model.compute_face_descriptor(uploaded_img, shape2)

            distance = sum((a - b) ** 2 for a, b in zip(desc1, desc2)) ** 0.5

            return Response({
                "face_distance": round(distance, 4),
                "match": distance < 0.6
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
