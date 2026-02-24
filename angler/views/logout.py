from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import logout, authenticate
from django.contrib import messages



class LogoutView(View):
    def get(self, request): #TODO switch to post after logout button has been added to html templates
        logout(request)
        return redirect('/') # eventual change to feed for non authenticated users (limited function that will display posts)

