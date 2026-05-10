from django.db import models
from django.utils import timezone
from angler.models.user import User
from angler.mixins import ImageRotateMixin
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class GroupChat(ImageRotateMixin, models.Model):
    """
    Group chat instance is created when a user messages another user for the first time. Group chat will house both users and any aditional users added thereafter.
    Group chat owner is the user that initiates the message. Users correspond to all other users added to the group chat.
    """
    image_field = 'image'

    group_name = models.CharField(max_length=128, default='Direct Message')
    image = models.ImageField( upload_to='gc_img/', blank=True, max_length=500)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='gc_owner')
    users = models.ManyToManyField(User, blank=True, related_name='gc_users')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.group_name
    
    def add_user(self, user_to_add):
        if self.users.count() < 20:
            self.users.add(user_to_add)
        else:
            raise ValueError('Group chat users cant exceed 20')    
    
    def new_owner(self):
        """
        When current group chat owner leaves the group chat or delets their account
        the group user in first position (of users) becomes the new owner. If a group chat has no users and the current
        owner leaves the gc or deletes his account, the group chat is 'soft' deleted.
        """
        if self.users.count() > 0:
            new_owner = self.users.all().first()
            self.owner = new_owner
            self.users.remove(new_owner)
        else:
            self.soft_delete_gc()

    def soft_delete_gc(self):
        """
        Set group chat deleted_at field to current date/time.
        Will be used to set a task to hard delete after 30 days.
        """
        from angler.tasks import hard_delete

        self.deleted_at = timezone.now()
        hard_delete.apply_async(args=[self.id], countdown=30*24*60*60)

    def leave_group_chat(self, user):
        """
        Remove user from group chat. If user is owner new_owner()
        is called to replace and or 'soft' delte group chat.
        """
        if self.owner == user:
            self.new_owner()
        elif self.users.filter(id=user.id).exists():
            self.users.remove(user)
        self.save()

    def set_default_image(self):
        """
        Upon creating a group chat, this helper is called and if no groupchat
        image is set, the default image is set to the owner user's profile image.
        """
        if not self.image:
            self.image = self.owner.get_profile_image()
            self.save()  

    def get_latest_message(self):
        """
        return latest message sent in group chat instance
        """
        return self.chat_messages.first() 
  
                
    class Meta:
        ordering = ['created_at']

class Reaction(models.Model):
        """
        Users can react to different objects (currently direct messages and reply direct messages), with generic foreignkey 
        reactions can be asociated and used with future added objects.
        """
        REACTION_CHOICES = [
        ('Heart', '❤️'),
        ('Thumbs Up', '👍'),
        ('Thumbs Down', '👎'),
        ('Fire', '🔥'),
        ('Crying', '😭'),
        ('Laughing', '😂'),
        ('Angled Laugh', '🤣')
    ]
        reaction = models.CharField(REACTION_CHOICES, max_length=20)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            obj = self.content_object
            if hasattr(obj, 'text'):
                return f"@{self.user.username} {self.reaction} reacted on @{self.content_object.author.username} message: {obj.text}"


class DirectMessage(ImageRotateMixin, models.Model):
    """
    Direct Messages are connected to a groupchat instance. A Direct message can be a normal message or a reply to a parent message.
    Direct Messages will be stored for 30 after a user deletes said message and or a group chat is deleted
    """
    image_field = 'image'

    group = models.ForeignKey(GroupChat, related_name='chat_messages', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='msg_author')
    text = models.CharField(max_length=300)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='msg_parent')
    image = models.ImageField(blank=True, upload_to='chat_img/')
    created_at = models.DateTimeField(auto_now_add=True)
    reaction = GenericRelation(Reaction)

    def __str__(self):
        return f"@{self.author.username}: {self.text}"

    def get_reaction_count(self):
        return self.reaction.count()    
    
    class Meta:
        ordering = ['-created_at']      
        