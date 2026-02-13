from django.db import models
from django.utils import timezone
from angler.models.user import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    # title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True) #for post edits
    post_image = models.ImageField (upload_to='profile_img/', null=False , blank=True)

    def publish(self):
        self.created_at = timezone.now()
        self.save() 

    # def __str__(self):
    #     return f"{self.author.username}'s post @: {self.created_at}"   