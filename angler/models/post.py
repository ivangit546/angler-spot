from django.db import models
from angler.models.user import User
from angler.mixins import ImageRotateMixin
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Post(ImageRotateMixin, models.Model):
    """
    User created posts, can be text and or images
    """
    image_field = 'image'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    image = models.ImageField (upload_to='post_img/', blank=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFit(1200, 675, upscale=False)], format='JPEG', options={'quality':70})

    def __str__(self):
        return f"@{self.user.username}'s post (post id: {self.id})"
    
    def is_liked(self, user):
        if Like.objects.filter(user=user, post_id=self.id).exists():
            return True
        else:
            return False
    @property
    def like_count(self):
        likes = Like.objects.filter(post=self).count()
        return likes
    
    @property
    def comment_count(self):
        comments = Comment.objects.filter(post=self).count()
        return comments    
        
class Comment(models.Model):
    """
    Represents comments on posts and or replies on parent comments/replies
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f"@{self.user.username}'s comments ({self.text[:30]}) on @{self.post.user.username}'s post (post_id: {self.post.pk} )"

    def is_liked(self, user):
        """
        Returns true if a comment and or reply has been liked by the user
        """
        if Like.objects.filter(user=user, comment_id=self.id).exists():
            return True
        else:
            return False
    @property
    def like_count(self):
        """
        Returns amount of likes comment and or reply has
        """
        likes = Like.objects.filter(comment=self).count()

        return likes
    @property
    def reply_count(self):
        """
        Return amount of child comments (replies) a comment and or reply has
        """
        reply_count = Comment.objects.filter(parent=self).count()

        return reply_count    

class Like(models.Model):
    """
    Represents a like to a comment or reply obj
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post_like')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='post_like')
    
    def __str__(self):
        if self.post:
            return f"@{self.user.username}'s like to post:{self.post.__str__()}"
        elif self.comment:
            return f"@{self.user.username}'s like to comment:{self.comment.__str__()}"

    def post_or_comment(self):
        """
        return if the like obj is a post or comment like
        """
        if self.post != None:
            return 'post'
        elif self.comment != None:
            return 'comment'
        else:
            return None
    
