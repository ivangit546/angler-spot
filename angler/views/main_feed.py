from django.shortcuts import redirect, render
from django.views import View
from angler.models.post import Post
from angler.forms.post import PostCommentCreateForm

class MainFeedView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        posts = Post.objects.order_by('-created_date')
        comment_form = PostCommentCreateForm()
        context = {
            'posts': posts,
            'comment_form':comment_form
        }
        return render(request, 'angler/main_feed.html', context)

