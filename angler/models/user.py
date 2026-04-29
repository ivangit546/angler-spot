from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import requests
from io import BytesIO

class User(AbstractUser):
    """
    Customer user class, for added fields 
        *is_confirmed: A user has clicked confirmation email and account is now confirmed
        *is_private: A user's posts, fishdex, tackle objects and profile is unviewable to non friend users
    """
    is_confirmed = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)

    @property
    def level(self):
        """
        Return a string representation of a user's level based on their points
        """
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
    
    def add_points(self, amount):
        """
        Take a user object and add amount to the user's points
        """
        self.points += amount
        self.save()

    def remove_points(self, amount):
        """
        Subtract passed in amount of points from a user's points
        """
        if self.points - amount < 0:
            self.points = 0
        else:
            self.points -= amount 
        self.save() 

    @property
    def get_profile_name(self):
        """
        Return user's asociated profile name 
        """
        return Profile.objects.get(user=self).profile_name
    
    def get_profile_image(self):
        """
        Return user's asociated profile image 
        """
        return Profile.objects.get(user=self).profile_image  

    def has_notification(self):
        return self.notifications.filter(is_read=False).exists()

class Profile(models.Model):
    """
    Every user has a profile that houses profile related content i.e profile name, image, bio
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_profile_img.jpg', upload_to='profile_img/', null=False, blank=True)
    profile_name = models.CharField(max_length=16, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.profile_name
   
    def save(self, *args, **kwargs):
        """
        Custom save(), if a user sets a profile image upon account creation and or profile edit, the image is resized and then saved
        """
        super().save(*args, **kwargs)
        response = requests.get(self.profile_image.url)
        image = Image.open(BytesIO(response.content))
        if image.height > 300 or image.width > 300:
            image.thumbnail((300, 300))
            output = BytesIO()
            image.save(output, format=image.format or 'JPEG')
            output.seek(0)
            self.profile_image.save(self.profile_image.name, output, save=False)
            super().save(*args, **kwargs)