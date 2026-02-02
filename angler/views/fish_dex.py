from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from angler.models.fish import Fish, FishDex, FishEntry

class FishDex_View(View):

    def get (self, request):
        user = self.request.user
        # user_fish_dex = FishDex.objects.get(user=user) might keep for clarification
        user_fishes = FishEntry.objects.filter(fish_dex=FishDex.objects.get(user=user)).all()
        locked_fishes = Fish.objects.exclude(id__in=user_fishes.values_list('fish_id'))
   
      
        return render(request, 'angler/fish_dex.html', {'user_fishes':user_fishes, 'locked_fishes': locked_fishes})
    

    def post(self, request):
        pass

