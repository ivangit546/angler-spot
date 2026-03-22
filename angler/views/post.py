from angler.models.post import Post, Comment, Like
from angler.forms.post import PostForm, PostCommentForm
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return redirect(request.META.get('HTTP_REFERER', 'default_url_name_or_path'))    

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
        return redirect(request.META.get('HTTP_REFERER', 'default_url_name_or_path'))

class DeleteCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)

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
 

class CreateReplyView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        form = PostCommentForm()
        parent_comment = get_object_or_404(Comment, id=comment_id)
        post = parent_comment.post
        top_replies = Comment.objects.filter(post=parent_comment.post, is_reply=True, parent=parent_comment)
        has_liked_comment = Like.objects.filter(comment=parent_comment, user=request.user).exists()
        has_liked_post = Like.objects.filter(post=post, user=request.user).exists()
        liked_reply_ids = set(Like.objects.filter(user=request.user).values_list('comment_id', flat=True))
        context = {'form':form,
                    'parent_comment':parent_comment,
                    'liked_comment':has_liked_comment,
                    'top_replies':top_replies,
                    'post':post,
                    'liked_post':has_liked_post,
                    'liked_reply_ids':liked_reply_ids}
        return render(request, 'angler/post/replies.html', context)
    
    def post(self, request, comment_id):
        parent = get_object_or_404(Comment, id=comment_id)
        post = parent.post
        reply_form = PostCommentForm(data=request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.parent = parent
            reply.is_reply = True
            reply.post = post
            reply.save()
        return redirect(request.META.get('HTTP_REFERER', 'default_url_name_or_path')) 

class PostDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostCommentForm()
        top_comments = Comment.objects.filter(post=post, is_reply=False)
        has_liked_post = Like.objects.filter(post=post, user=request.user).exists()
        liked_top_comment_ids = set(Like.objects.filter(user=request.user).values_list('comment_id', flat=True))
        context = {
            'form':form,'post':post,
            'top_comments':top_comments,
            'liked_post':has_liked_post, 
            'liked_comment_ids':liked_top_comment_ids

        }
        return render(request, 'angler/post/post_detail.html', context)    

