from django.db import models
from angler.models.user import User

class FriendList(models.Model):
    """
    Collection of Users who are friends with User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}'s friendlist"

    def add_friend(self, account):
        """
        Adds a friend, if realtionship doesn't exist yet
        """
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def unfriend(self, account):
        """
        Initiate friem removal from both users in the friend relationship
        """
        self.remove_friend(account)
        account_friendlist = FriendList.objects.get(user=account)
        account_friendlist.remove_friend(self.user)


    def remove_friend(self, friend):
       """
       Removes a friend if the relationship exists
       """
       if friend in self.friends.all():
           self.friends.remove(friend)
           self.save()
       if FriendRequest.objects.filter(request_sender=self.user, request_reciever=friend).exists():
           FriendRequest.objects.get(request_sender=self.user, request_reciever=friend).delete_request()
            
    def is_friend(user1, user2):
        """
        Check if user is friends with second user, return boolean value
        """
        user_friend_list = FriendList.objects.get(user=user1)
        friends = user_friend_list.friends.all()
        for friend in friends:
            if friend == user2:
                return True 
            
    def private(user1, user2):
        """
        Return True if user1 is not friends with user2 and is private // return true if user2 will have access to view user's profile, fishdex...
        """
        if user1 != user2 and not FriendList.is_friend(user1, user2):
            if user2.is_private:
                return True
        return False         
        
    def __str__(self):
        return f"{self.user}'s friendlist"   
            
           
class FriendRequest(models.Model):
    """
    Represents initial step to adding users to a user's friendlist.
    Friend request will be in 1 of 2 states: pending(sent request that has not been accepted/rejected), accepted(a user is added to user's friendlist)
    """ 
    STATUS_CHOICES = ((0,'Pending'),
                      (1, 'Accepted')
                     )
    request_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    request_reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_reciever')
    request_status = models.IntegerField( default=0, choices= STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_sender.username}'s friend request to {self.request_reciever.username}"

    def accept_request(self):
        """
        Accept Friend Request.
        Add friend request sender to reciever's friendlist.
        Add friend request reciever to sender's friendlist.
        """
        reciever_friendlist = FriendList.objects.get(user=self.request_reciever)
        if reciever_friendlist:
            reciever_friendlist.add_friend(self.request_sender)
            self.request_status = 1
            sender_friendlist = FriendList.objects.get(user=self.request_sender)
            if sender_friendlist:
                sender_friendlist.add_friend(self.request_reciever)
                self.save()
       
    def delete_request(self):
        """
        Delete friend request.
        """
        self.delete()
