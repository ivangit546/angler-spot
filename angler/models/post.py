from django.db import models
from django.utils import timezone
from angler.models.user import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    image = models.ImageField (upload_to='post_img/', blank=True)

    def __str__(self):
        return f"@{self.author.username}'s post @: {self.created_date}"   
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    #TODO implement replies where a reply would have a parent comment and so on 

    def __str__(self):
        return f"@{self.user.username}'s comment on @{self.post.user.username}'s post (post_id: {self.post.pk} )"