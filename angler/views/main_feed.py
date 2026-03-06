from django.shortcuts import redirect, render
from django.views import View
from angler.models.post import Post
from angler.forms.post import PostCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class MainFeedView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        posts = Post.objects.order_by('-created_date')
        comment_form = PostCommentForm()
        context = {
            'posts': posts,
            'comment_form':comment_form
        }
        return render(request, 'angler/main_feed.html', context)

