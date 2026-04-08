from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models.user import User, Profile
from angler.models.post import Post
from angler.models.friends import FriendList, FriendRequest
from django.shortcuts import get_object_or_404, get_list_or_404

class UserProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_profile = get_object_or_404(Profile, user=user)
        posts = Post.objects.filter(user=user)
        is_users_acc = False
        if user == request.user:
            is_users_acc = True
        is_friend = FriendList.is_friend(user, request.user)
        pending_sent_friend_request = FriendRequest.objects.filter(request_sender=request.user, request_reciever=user, request_status=0).exists()  
        pending_recieved_friend_request = FriendRequest.objects.filter(request_sender=user, request_reciever=request.user, request_status=0).exists()       
        context = {
            'user':user,
            'user_profile':user_profile,
            'posts':posts,
            'is_users_acc':is_users_acc,
            'is_friend':is_friend,
            'pending_sent_friend_request':pending_sent_friend_request,
            'pending_recieved_friend_request':pending_recieved_friend_request
        }
        return render(request, 'angler/user/user_profile.html', context)
        