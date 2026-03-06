from angler.models.post import Post, Comment, Like
from angler.forms.post import PostForm, PostCommentForm
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Count
from django.conf import settings

class CreatePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        post_form = PostForm()
        return render(request, 'angler/post.html', {'post_form':post_form})
    def post(self, request):
        user = request.user
        post_form = PostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.save()
        return redirect('/')
    
class DeletePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return redirect('/')
    
class CreateCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_form = PostCommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post 
            comment.save()
        return redirect('/')

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        parent = get_object_or_404(Comment, id=comment_id)
        text = request.POST.get('text')
        Comment.objects.create(
            post=parent.post,
            user=request.user,
            text=text,
            parent=parent,
            is_reply=True
        )
        return redirect('post_detail', post_id=parent.post_id) 

class PostDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        top_comments = Comment.objects.filter(post=post, is_reply=False)
        liked_post = Like.objects.filter(post=post, user=request.user).exists()
        liked_top_comment_ids = set(Like.objects.filter(user=request.user).values_list('comment_id', flat=True))
        context = {
            'post':post,
            'top_comments':top_comments,
            'liked_post':liked_post,
            'liked_comment_ids':liked_top_comment_ids

        }
        return render(request, 'angler/post_detail.html', context)    

class LikePostView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, post_id):
        user=request.user
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=user, post_id=post_id)
        if like:
            like.delete() 
        else:
            Like.objects.create(user=user, post=post)    
        return redirect('post_detail', post_id=post_id)

class UnLikeCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        Like.objects.filter(user=request.user, comment=comment).delete()
        return redirect(request.META.get('HTTP_REFERER', 'default_url_name_or_path'))
    
class LikeCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, comment_id):
        user = request.user
        comment = get_object_or_404(Comment, id=comment_id)
        like = Like.objects.filter(user=user, comment_id=comment_id)
        if like:
            like.delete() 
        else:
            Like.objects.create(user=user, comment=comment) 
        return redirect(request.META.get('HTTP_REFERER', 'default_url_name_or_path'))


    
class DeleteCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return redirect('/')
    
# class EditCommentView(LoginRequiredMixin, UpdateView):
#     login_url = '/login/'
#     model = Comment
#     form_class = PostCommentForm
#     success_url = '/'


