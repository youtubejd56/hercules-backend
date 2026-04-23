from django.db import models
from django.contrib.auth.models import User

class ImagePost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Admission(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    plan = models.CharField(max_length=50, default='Pro')
    status = models.CharField(max_length=20, default='Pending')
    profile_pic = models.ImageField(upload_to='members/', null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    last_payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=5)
    role = models.CharField(max_length=50, default='Member')
    duration = models.CharField(max_length=50, default='1 Yr')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    GOAL_CHOICES = [
        ('lose_fat', 'Lose Fat'),
        ('build_muscle', 'Build Lean Muscle'),
        ('learn_body', 'Learn About My Body'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, default='')
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
