from django.shortcuts import redirect, render
from django.views import View
from angler.models import Post, User, Profile
from angler.forms.user import UserRegistrationForm, ProfileForm
from django.contrib.auth import login



class Login_View(View):    
    def get(self, request):
        return render(request, 'angler/login.html')    
