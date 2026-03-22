from angler.models.user import User
from angler.models.friends import FriendList, FriendRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class FriendsListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        friend_requests = FriendRequest.objects.filter(request_reciever=request.user,request_status=0 )
        user = User.objects.get(id=user_id)

        friends = FriendList.objects.get(user=user).friends.all()
        context = {
            'friends':friends,
            'friend_requests':friend_requests
        }
        return render(request, 'angler/friend.html', context)

class SendFriendRequestView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, user_id):
        user_sender = request.user
        user_reciever = get_object_or_404(User, id=user_id)

        if user_sender != user_reciever and FriendList.objects.filter(friends=user_reciever).exists() == False:
            FriendRequest.objects.create(request_sender=user_sender, request_reciever=user_reciever)
        return redirect('user_profile', user_id=user_reciever.id)    
    
class ManageFriendRequestView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, user_id):
        user_sender = get_object_or_404(User, id=user_id)
        user_reciever = request.user
        action = request.POST.get('action')
        friend_request = get_object_or_404(FriendRequest, request_reciever=user_reciever, request_sender=user_sender, request_status=0)

        if action == 'accept':
            friend_request.accept_request()
        elif action == 'reject':
            friend_request.delete_request()
        return redirect('friendslist',user_id=user_reciever.id) 

class RemoveFriendView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, user_id):
        user_to_remove = get_object_or_404(User, id=user_id)
        users_friendlist = get_object_or_404(FriendList, user=request.user)
        users_friendlist.unfriend(user_to_remove)
        return redirect('user_profile', user_id=user_to_remove.id)    
      