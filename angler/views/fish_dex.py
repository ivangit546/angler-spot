from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.user import User
from angler.models.friends import FriendList
from angler.forms.fish_dex import FishDexEntryForm
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import JsonResponse, Http404


class FishDexView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get (self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if FriendList.private(request.user, user):
            raise Http404("Page not found")
        fish_entries = FishEntry.objects.filter(fish_dex=FishDex.objects.get(user_id=user_id))
        locked_fish = Fish.objects.exclude(id__in=fish_entries.values_list('fish_id'))
        all_fish = Fish.objects.all()
        context = { 'user':user,
                    'fish_entries':fish_entries,
                    'locked_fish':locked_fish,
                    'all_fish':all_fish}
      
        return render(request, 'angler/fishdex/fish_dex.html', context)
    
class FishDexDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get (self, request, fishdex_id, fish_entry_id): 
        fish_entry = get_object_or_404(FishEntry, id=fish_entry_id, fish_dex_id=fishdex_id) 
        user = fish_entry.fish_dex.user 
        if FriendList.private(request.user, user):
            raise Http404("Page not found")
        context = { 'user':user,
                   'fish_entry':fish_entry,
                   'fish_color':fish_entry.get_fish_color
                   }    
        return render(request, 'angler/fishdex/detail.html', context)    
    

class FishDexEntryView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        form = FishDexEntryForm()
        form.fields['fish'].queryset = Fish.objects.exclude(
            id__in=FishEntry.objects.filter(fish_dex=FishDex.objects.get(user_id=request.user.id)).all()
            .values_list('fish_id')) # only want user to see locked fish in options of fish to enter in their fishdex
        
        return render(request, 'angler/fishdex/create.html',{'form':form})

    def post(self, request):
        user = request.user
        fish_dex = FishDex.objects.get(user=user)
        fish_entry_form = FishDexEntryForm(data=request.POST, files=request.FILES)
        if fish_entry_form.is_valid():
            fish_entry = fish_entry_form.save(commit=False)
            fish_entry.fish_dex = fish_dex
            if request.FILES.get('fish_dex_image'):
                fish_entry.thumbnail = request.FILES.get('fish_dex_image')
            fish_entry.save()
            if fish_entry.fish.shiny:
                fish_dex.user.add_points(100)
            else:
                fish_dex.user.add_points(50)    
            fish_dex.unlocked +=1
            fish_dex.save()
            return redirect('fishdex', user_id=user.id)
            
class FishEntryLocation(LoginRequiredMixin, View):
    login_url = '/login/'    
    def post(self, request, fish_entry_id):
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if not all([latitude, longitude]):
                return JsonResponse({
                'status': 'error',
                'message': 'Incomplete location data'
            }, status=400)
            fish_dex = get_object_or_404(FishDex, user=request.user)
            FishEntry.objects.filter(pk=fish_entry_id, fish_dex=fish_dex).update(
                latitude=latitude,
                longitude=longitude
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Location saved'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            print('ERROR:', e)
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

class FishDexEntryDelete(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, entry_id):
        fish_dex = get_object_or_404(FishDex, user=request.user)
        entry = get_object_or_404(FishEntry, id=entry_id, fish_dex=fish_dex)
        if request.user != fish_dex.user:
            raise Http404('Cannot delete another user''s entry')
        entry.delete()
        fish_dex.lock()
        if entry.fish.shiny:
            fish_dex.user.remove_points(100)
        else:
            fish_dex.user.remove_points(50)    
 
        return redirect('fishdex', user_id=request.user.id)

