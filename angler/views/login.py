from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



class LoginView(View):    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect ('/')
        form = AuthenticationForm(request)
        return render(request, 'angler/login.html', {'form':form})  

    def post(self, request): #TODO add email as option for authentication -> implement custom backend
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        else:
            messages.error(request, ("Enter a valid username and password"))
            return redirect('login')
