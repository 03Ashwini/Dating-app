from django.contrib.auth.models import AbstractUser
from django.db import models


# ✅ Custom User Model (Using Email as Username)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Still need a username

    def __str__(self):
        return self.email


# ✅ Profile Model (To Store Additional User Info)
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
