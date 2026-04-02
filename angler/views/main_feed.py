from django.shortcuts import redirect, render
from django.views import View
from angler.models.post import Post, Like
from angler.forms.post import PostCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class MainFeedView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        posts = Post.objects.order_by('-created_date')
        comment_form = PostCommentForm()
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        context = {
            'posts': posts,
            'liked_post_ids':liked_post_ids,
            'comment_form':comment_form
        }
        return render(request, 'angler/main_feed.html', context)

class AboutUsView(View):
    def get(self, request):
        return render(request, 'angler/about_us.html')