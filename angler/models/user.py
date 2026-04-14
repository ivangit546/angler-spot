from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from PIL import Image
class User(AbstractUser):
    is_private = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0) #previous idea have a cap on points validators=[MaxValueValidator(5000)]
    @property
    def level(self):
        if self.points <= 0:
            return 'None'
        elif self.points <= 999:
            return 'Bronze'
        elif self.points <= 1999:
            return 'Silver'
        elif self.points <= 2999:
            return 'Gold'
        elif self.points <= 3999:
            return 'Diamond'
        else:
            return 'Platinum'
        

    def __str__(self):
        return self.username
    
    def add_login_points(self):
        self.points += 10
        self.save()
        
    @property
    def get_profile_name(self):
        return Profile.objects.get(user=self).profile_name
    
    def get_profile_image(self):
        return Profile.objects.get(user=self).profile_image
    # def liked_post(self):
    #     return Comment

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_profile_img.jpg', upload_to='profile_img/', null=False, blank=True)
    profile_name = models.CharField(max_length=16, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.profile_name
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.profile_image.path)
        if image.height > 300 or image.width > 300:
            image.thumbnail((300,300))
            image.save(self.profile_image.path)