from django.shortcuts import redirect, render
from django.views import View
from .models import Post, User, Profile
# from django.contrib import messages
from angler.forms.user import UserRegistrationForm

class MainFeed_View(View):

    def get(self, request):
        # if not request.user.is_authenticated:
        #     messages.error(request, 'Log in or register to view the feed')       
        posts = Post.objects.order_by('created_date')
        context = {
            'posts': posts
        }
        return render(request, 'angler/post_list.html', context)


class Register_View(View):
    
    def get(self, request):
        user_form = UserRegistrationForm
        return render(request, 'angler/register.html', {'user_form':user_form})
    
    def post(request):
        user_form = UserRegistrationForm(data=request.post)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            Profile.objects.create()
        else:
            print(user_form.errors)
        return redirect('/login/')        
    
class Login_View(View):
    
    def get(self, request):
        return render(request, 'angler/login.html')    

