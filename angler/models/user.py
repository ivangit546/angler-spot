from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

class User(AbstractUser):
    # level = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    # points = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5000)])
    def __str__(self):
        return self.username
    
    # def level_up(self):

    #     pass
    #TODO point system each entry in the fishdex will be 25 if non shiny and 50 points if shiny
        # plan max level=100 and max points with planned (50 fish atm) total of a max 4500 points
        # account data to be dynamic as more types of fish are added to db 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_profile_img.jpg', upload_to='profile_img/', null=False, blank=True)
    profile_name = models.CharField(max_length=16, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.profile_name
    #TODO add point system for the user that will be based on unlocked fish in their fishdex

