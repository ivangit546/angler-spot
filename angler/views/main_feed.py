from django.shortcuts import redirect, render
from django.views import View
from angler.models import Post, User, Profile
from django.contrib.auth import login

class MainFeed_View(View):

    def get(self, request):
        # if not request.user.is_authenticated:
        #     messages.error(request, 'Log in or register to view the feed')       
        posts = Post.objects.order_by('created_date')
        context = {
            'posts': posts
        }
        return render(request, 'angler/main_feed.html', context)

