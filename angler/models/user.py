from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_profile_img.jpg', upload_to='profile_img/', null=False, blank=True)
    profile_name = models.CharField(max_length=16, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.profile_name