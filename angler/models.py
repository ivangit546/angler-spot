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
    profile_name = models.CharField(max_length=16, blank=False, null=False)
    bio = models.TextField(max_length=500, blank=True)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True) #for post edits
    post_image = models.ImageField (upload_to='profile_img/', null=False , blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save() 

    def __str__(self):
        return self.title    
    
