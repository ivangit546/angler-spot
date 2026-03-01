from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.user import User
from angler.forms.fish_dex import FishDexEntryForm

class FishDexView(View):

    def get (self, request, user_id):
        is_users_account = False
        user = get_object_or_404(User, id=user_id)
        if user.id == user_id: 
            is_users_account = True
        # user_fish_dex = FishDex.objects.get(user=user) might keep for clarification
        user_fishes = FishEntry.objects.filter(fish_dex=FishDex.objects.get(user_id=user_id))
        locked_fishes = Fish.objects.exclude(id__in=user_fishes.values_list('fish_id'))
        context = { 'user':user,
                    'user_fishes':user_fishes,
                    'locked_fishes': locked_fishes,
                    'is_users_account':is_users_account}
      
        return render(request, 'angler/fish_dex.html', context)
    

class FishDexEntryView(View):

    def get(self, request):
        form = FishDexEntryForm()
        form.fields['fish'].queryset = Fish.objects.exclude(
            id__in=FishEntry.objects.filter(fish_dex=FishDex.objects.get(user_id=request.user.id)).all()
            .values_list('fish_id')) # only want user to see locked fish in options of fish to enter in their fishdex
        
        return render(request, 'angler/fish_dex_entry.html',{'form':form})

    def post(self, request):
        user = request.user
        fish_dex = FishDex.objects.get(user=user)
        fish_dex_id = fish_dex.id
        print("id number: " + str(fish_dex_id))
        fish_entry_form = FishDexEntryForm(data=request.POST, files=request.FILES)
        if fish_entry_form.is_valid():
            fish_entry = fish_entry_form.save(commit=False)
            fish_entry.fish_dex = fish_dex
            fish_entry.save()
            fish_dex.unlocked +=1 
            fish_dex.save()
            return redirect('fishdex', user_id=user.id)
        
# class FishDexEntryEdit(View):
#     def post(self, request):
#         pass