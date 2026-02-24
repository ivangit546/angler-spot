from angler.models.user import User
from angler.models.friends import FriendList, FriendRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


class FriendsListView(View):
    def get(self, request, user_id):
        request_user = request.user
        user = User.objects.get(id=user_id)
        is_user = False
        is_private = False

        if user == request_user:
            is_user = True
        else:
            is_private = user.is_private

        friends = FriendList.objects.get(user=user).friends.all()
        context = {
            'friends':friends,
            'is_user':is_user,
            'is_private':is_private
        }
        return render(request, 'angler/friend.html', context)

class SendFriendRequestView(View):
    def post(self, request, user_id):
        user_sender = request.user
        user_reciever = get_object_or_404(User, id=user_id)

        if user_sender != user_reciever and FriendList.objects.filter(friends=user_reciever).exists() == False:
            FriendRequest.objects.create(request_sender=user_sender, request_reciever=user_reciever)
        return redirect('user_profile', user_id=user_reciever.id)    
    
class ManageFriendRequestView(View):
    def post(self, request, user_id):
        user_sender = get_object_or_404(User, id=user_id)
        user_reciever = request.user
        action = request.POST.get('action')
        friend_request = get_object_or_404(FriendRequest, request_reciever=user_reciever, request_sender=user_sender, request_status=0)

        if action == 'accept':
            friend_request.accept_request()
        elif action == 'reject':
            friend_request.reject_request()
        return redirect('friendslist',user_id=user_reciever.id) 

class RemoveFriendView(View):
    def post(self, request, user_id):
        pass    
      