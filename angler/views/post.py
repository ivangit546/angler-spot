from angler.models.user import User
from angler.models.post import Post
from django.views import View

class CreatePostView(View):
    def post(self, request):
        pass
class DeletePostView(View):
    def post(self, request, post_id):
        pass

class LikePostView(View):
    def post(self, request, post_id):
        pass

class CreateCommentView(View):
    def post(self, request, post_id):
        pass
    
class DeleteCommentView(View):
    def post(self, request, post_id):
        pass        

