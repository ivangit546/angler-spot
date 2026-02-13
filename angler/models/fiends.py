from django.db import models
from angler.models.user import User

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.user.username}'s friendlist"


class FriendRequest(models.Model):
    STATUS_CHOICES = (('Pending', 0)
                      ('Accept', 1),
                      ('Reject', 2))
    request_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    request_reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    request_status = models.IntegerChoices(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_sender.username}'s friend request to {self.request_reciever.user}"

    def accept_request(self):
        reciever_friendlist = FriendList.objects.get(user=self.request_reciever)
        if reciever_friendlist:
            reciever_friendlist # call helper method that would add this user to the senders friendlist
            # repeat helper method call to add sender to the reciever's friendlist 
