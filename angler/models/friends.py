from django.db import models
from angler.models.user import User

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}'s friendlist"

    def add_friend(self, account):
        account_friendlist = FriendList.objects.get(user=account)
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def unfriend(self, account):
        self.remove_friend(account)
        self.save()
        account_friendlist = FriendList.objects.get(user=account)
        account_friendlist.remove_friend(account)
        account_friendlist.save()

    def remove_friend(self, friend):
        if self.friends.filter(pk=friend.pk).exists():    
            self.friends.remove(friend)
            
            if FriendRequest.objects.filter(request_sender=self.user, request_reciever=friend).exists():
                FriendRequest.objects.get(request_sender=self.user, request_reciever=friend).delete_request()
        self.save()

            
    def is_friend(user1, user2):
        user_friend_list = FriendList.objects.get(user=user1)
        friends = user_friend_list.friends.all()
        for friend in friends:
            if friend == user2:
                return True 
        
    def __str__(self):
        return f"{self.user}'s friendlist"
class FriendRequest(models.Model):
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
        reciever_friendlist = FriendList.objects.get(user=self.request_reciever)
        if reciever_friendlist:
            reciever_friendlist.add_friend(self.request_sender)
            self.request_status = 1
            sender_friendlist = FriendList.objects.get(user=self.request_sender)
            if sender_friendlist:
                sender_friendlist.add_friend(self.request_reciever)
                self.save()

            
    # def reject_request(self):
    #     self.delete()

    def delete_request(self):
        self.delete()
