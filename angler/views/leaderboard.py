from angler.models.user import User
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.cache import cache
from angler.tasks import update_leaderboard
class LeaderboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        top_users = cache.get('top_ten')
        if top_users == None:
            top_users = User.objects.order_by('-points')[:10]
            update_leaderboard.delay()
        return render(request, 'angler/leaderboard.html', {'users':top_users})