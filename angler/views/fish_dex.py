from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.user import User
from angler.forms.fish_dex import FishDexEntryForm

class FishDex_View(View):

    def get (self, request, user_id):
        req_user = self.request.user
        is_users_account = False
 
        if req_user.id == user_id: # will be useful info to know when I later add an add fish to fishdex button for a user on their own fishdex
            is_users_account = True

        # user_fish_dex = FishDex.objects.get(user=user) might keep for clarification
        user_fishes = FishEntry.objects.filter(fish_dex=FishDex.objects.get(user_id=user_id)).all()
        locked_fishes = Fish.objects.exclude(id__in=user_fishes.values_list('fish_id'))
   
      
        return render(request, 'angler/fish_dex.html', {'user_fishes':user_fishes, 'locked_fishes': locked_fishes, 'is_users_account':is_users_account})
    

class FishDexEntry(View):

    def get(self, request):
        form = FishDexEntryForm
        return render(request, 'angler/fish_dex_entry.html',{'form':form})

    def post(self, request):
        user = request.user
        fish_dex = FishDex.objects.get(user=user)
        fish_dex_id = fish_dex.id
        print("id number: " + str(fish_dex_id))
        fish_entry_form = FishDexEntryForm(data=request.POST, files=request.FILES)
        if fish_entry_form.is_valid():
            fish_entry_form = fish_entry_form.save(commit=False)
            fish_entry_form.fish_dex = fish_dex
            fish_entry_form.save()
            return redirect('fishdex', user_id=user.id)
        
