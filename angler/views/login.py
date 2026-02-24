from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages



class LoginView(View):    
    def get(self, request):
        if request.user is not None and request.user.is_authenticated:
            return redirect ('/')
        return render(request, 'angler/login.html')  

    def post(self, request): #TODO add email as option for authentication -> implement custom backend
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.error(request, ("Enter a valid username and password"))
            return redirect('login')
