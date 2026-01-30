from django.shortcuts import redirect, render
from django.views import View
from .models import Post, User, Profile
from .forms.user import UserRegistrationForm, ProfileForm
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


class Register_View(View):
    
    def get(self, request):
        user_form = UserRegistrationForm
        profile_form = ProfileForm
        return render(request, 'angler/register.html', {'user_form':user_form, 'profile_form':profile_form})
    
    def post(request):
        user_form = UserRegistrationForm(data=request.post)
        profile_form = ProfileForm(data=request.post, files=request.files)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False) #stop django from saving this instance of profile into the database without a user object in its one to one relationship yet
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('login')
        else:
            print(user_form.errors, profile_form.errors)
        return render(request, 'angler/register.html', {'user_form':user_form, 'profile_form':profile_form})        
    
class Login_View(View):    
    def get(self, request):
        return render(request, 'angler/login.html')    

