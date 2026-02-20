from django.db import models
from angler.models.user import User

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}'s friendlist"

    def add_friend(self, account):
        account_friendlist = FriendList.objects.get(user=account)
        if account not in self.friends.all() and self.user not in account_friendlist:
            self.friends.add(account)
            self.save()

            account_friendlist.friends.add(self.user)
            account_friendlist.save()

    def remove_friend(self, friend):
        if self.friends.filter(pk=friend.pk).exists():    
            self.friends.remove(friend)
            self.save()
            
    def is_friend(self, account):
        if self.friends.filter(pk=account.pk).exists():
                return True
            
class FriendRequest(models.Model):
    STATUS_CHOICES = (('Pending', 0),
                      ('Accept', 1),
                      ('Reject', 2))
    request_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    request_reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_reciever')
    request_status = models.IntegerField(choices= STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_sender.username}'s friend request to {self.request_reciever.user}"

    def accept_request(self):
        reciever_friendlist = FriendList.objects.get(user=self.request_reciever)
        if reciever_friendlist:
            reciever_friendlist.add_friend(self.request_reciever)
            sender_friendlist = FriendList.objects.get(user=self.request_sender)
            if sender_friendlist:
                sender_friendlist.add_friend(self.request_reciever)
                self.status = 0
                self.save()
                return True
            
    def reject(self):
        self.status = 2
        self.save()

    def cancel(self, friend_request):
        friend_request.delete()
                    