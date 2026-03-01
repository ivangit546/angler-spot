from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import logout, authenticate
from django.contrib import messages



class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/') # eventual change to feed for non authenticated users (limited function that will display posts)

