from angler.models.user import User
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class LeaderboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        pass