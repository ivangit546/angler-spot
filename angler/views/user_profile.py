from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models.user import User, Profile
from angler.models.post import Post, Like
from angler.models.friends import FriendList, FriendRequest
from django.shortcuts import get_object_or_404
from django.forms import modelform_factory
from django.contrib import messages

class UserProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    EditProfileForm = modelform_factory(Profile, fields=['profile_name', 'profile_image', 'bio',])
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_profile = get_object_or_404(Profile, user=user)
        posts = Post.objects.filter(user=user).order_by('-created_date')
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        is_friend = FriendList.is_friend(user, request.user)
        pending_sent_friend_request = FriendRequest.objects.filter(request_sender=request.user, request_reciever=user, request_status=0).exists()  
        pending_recieved_friend_request = FriendRequest.objects.filter(request_sender=user, request_reciever=request.user, request_status=0).exists()
        edit_form = self.EditProfileForm(instance=user_profile)
        context = {
            'user':user,
            'user_profile':user_profile,
            'posts':posts,
            'liked_post_ids':liked_post_ids,
            'is_friend':is_friend,
            'edit_form':edit_form,
            'pending_sent_friend_request':pending_sent_friend_request,
            'pending_recieved_friend_request':pending_recieved_friend_request
        }
        return render(request, 'angler/user/user_profile.html', context)
    def post (self, request, user_id):
        profile = get_object_or_404(Profile, user=request.user)
        edit_form = self.EditProfileForm(request.POST, request.FILES, instance=profile)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Profile Edit Successful')
        return redirect(request.path)
