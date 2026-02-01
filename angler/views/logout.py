from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import logout, authenticate
from django.contrib import messages



class Logout_View(View):
    def post(self, request):
        logout(request)
        return redirect('logout') # eventual change to feed for non authenticated users (limited function that will display posts)

