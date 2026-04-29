from django.db import models
from angler.models.user import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints =[
            models.CheckConstraint(
                condition=~models.Q(recipient=models.F('sender')),
                name='prevent notifications from self'
            )
        ]
        
    def __str__(self):
        return f"{self.message}"    
    
    def get_type(self):
        """
        return generic fk type (i.e. like, comment or friendrequest)
        """
        return self.content_type.model
    
    def get_like_notification_type(self):
        """
        return if a like notification belongs to a post or comment (if comment return comment or reply)
        """
        if self.content_type.model != 'like':
            return None
        like = self.content_object
        if like.post:
            return 'post'
        elif like.comment.is_reply:
            return 'reply'
        elif like.comment.is_reply == False:
            return 'comment'
        else: 
            return None

    def get_like_comment_or_reply_notification_type(self):
        """
        return if a comment type notificatino is a parent comment or reply 
        """
        if self.content_type.model != 'comment':
            return None
        comment = self.content_object
        if comment.is_reply:
            return 'reply'
        else:
            return 'comment'   

    def get_notification_url(self):
        obj =self.content_object
        model = self.content_type.model
        if model == None:
            return None
        if model == 'like':
            if obj.post:
                return reverse('post_detail', kwargs={'post_id': obj.post.id}) 
            if obj.comment and obj.comment.is_reply == False:
                return reverse('post_detail', kwargs={'post_id': obj.comment.post.id})
            if obj.comment.is_reply == True:
                return reverse('reply_create', kwargs={'comment_id': obj.parent.id})
        elif model == 'comment':
            if obj.is_reply == False:
                return reverse('post_detail', kwargs={'post_id': obj.post.id})
            else:
                return reverse('reply_create', kwargs={'comment_id': obj.parent.id})
        elif model == 'friendrequest':
                return reverse('user_profile', kwargs={'user_id': obj.request_sender.id})
        else:
            return None


    