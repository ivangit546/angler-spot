from angler.models.user import User
from angler.models.post import Post, Comment, Like
from angler.forms.post import PostCreateForm, PostCommentCreateForm
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render

class CreatePostView(View):
    def get(self, request):
        post_form = PostCreateForm()
        return render(request, 'angler/post.html', {'post_form':post_form})
    def post(self, request):
        user = request.user
        post_form = PostCreateForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.save()
        return redirect('/')
    
class DeletePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return redirect('/')
        
class LikePostView(View):
    def post(self, request, post_id):
        user=request.user
        post = get_object_or_404(Post, id=post_id)
        if not post.is_liked(user):
            Like.objects.create(user=user, post=post)
        return redirect('/')
     
# class LikeCommentView(View):
#     def post(self, request, comment_id):
#         comment = get_object_or_404(Post, id=comment_id)
#         Like.objects.create(user=request.user, comment=comment)
#         return redirect('/')
    
class CreateCommentView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_form = PostCommentCreateForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post 
            comment.save()
        return redirect('/')
    
class DeleteCommentView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return redirect('/')

