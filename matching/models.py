from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_user2')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} ❤ {self.user2.username}"

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate matches


class LikeDislike(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    is_liked = models.BooleanField()  # True for Like, False for Dislike
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Prevent repeated like/dislike

    def __str__(self):
        status = "Like" if self.is_liked else "Dislike"
        return f"{self.from_user.username} ➡ {self.to_user.username} ({status})"
