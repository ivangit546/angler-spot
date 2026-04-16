from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404
from angler.models.fish import FishDex, FishEntry
from angler.models.user import User
from angler.models.friends import FriendList
from angler.models.tackle import RodAndReel, Lure
from angler.forms.tackle import RodAndReelForm, LureForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

class TackleView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if FriendList.private(request.user, user):
            raise Http404("Page not found")
        rod_and_reels = RodAndReel.objects.filter(user=user)
        lures = Lure.objects.filter(user=user)
        context ={'user':user,
                   'rod_and_reels':rod_and_reels,
                     'lures':lures}
        return render(request, 'angler/tackle/tacklebox.html', context)

class TackleDetailView(LoginRequiredMixin, View):
    login_url = '/login'
    def get(self, request, tackle_type, tackle_id):
        if tackle_type == 'lure':
            tackle_obj = get_object_or_404(Lure, id=tackle_id)
            fish_entries = FishEntry.objects.filter(lure=tackle_obj)
        elif tackle_type == 'rod':
            tackle_obj = get_object_or_404(RodAndReel, id=tackle_id) 
            fish_entries = FishEntry.objects.filter(tackle=tackle_obj)
        else:
            raise ValueError('Invalid tackle type')
        if FriendList.private(request.user, get_object_or_404(User,id=tackle_obj.user.id)):
            raise Http404("Page not found")        
        context = {'tackle_obj': tackle_obj,
                    'tackle_type':tackle_type,
                    'fish_entries':fish_entries}
        return render(request, 'angler/tackle/detail.html',context)
    
        
class RodAndReelCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get (self, request):
        form = RodAndReelForm()
        return render(request, 'angler/tackle/rod_and_reel/create.html', {'form':form})
    
    def post(self, request):
        user = request.user
        rod_and_reel_form = RodAndReelForm(data=request.POST)
        if rod_and_reel_form.is_valid():
            rod_and_reel = rod_and_reel_form.save(commit=False)
            rod_and_reel.user = user
            rod_and_reel.save()
        return redirect('tackle', user.id)    
    
class LureCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self,request):
        form = LureForm()
        return render(request, 'angler/tackle/lure/create.html', {'form':form})

    def post(self, request):
        user = request.user
        lure_form = LureForm(data=request.POST)
        if lure_form.is_valid():
            lure = lure_form.save(commit=False)
            lure.user = user
            lure.save()
        return redirect('tackle', user.id)
    
class TackleEntryAdd(LoginRequiredMixin, View):
    login_url ='/login/'
    def get(self, request, tackle_type, fish_entry_id,):
        user = request.user
        fish_entry = get_object_or_404(FishEntry, id=fish_entry_id)
        if tackle_type == 'lure':
            tackle_objs = Lure.objects.filter(user=user)
        else:
            tackle_objs = RodAndReel.objects.filter(user=user)  
        context ={'user':user,
                   'tackle_objs':tackle_objs,
                     'fish_entry':fish_entry,
                     'tackle_type':tackle_type}
        return render(request, 'angler/tackle/add.html', context)
    
    def post(self, request, tackle_type, tackle_id, fish_entry_id):
        user = request.user
        fishdex = get_object_or_404(FishDex, user=user)
        fish_entry = get_object_or_404(FishEntry, id=fish_entry_id, fish_dex=fishdex)
        if tackle_type == 'lure':
            lure = get_object_or_404(Lure, id=tackle_id, user=user)
            fish_entry.lure = lure
        else:
            rod_reel = get_object_or_404(RodAndReel, id=tackle_id, user=user)
            fish_entry.tackle = rod_reel
        fish_entry.save()
        return redirect ('fishdex_detail',fishdex.id, fish_entry_id )

class DeleteTackleView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, tackle_type, tackle_id):
        if tackle_type == 'lure':
            tackle_obj = get_object_or_404(Lure, id=tackle_id)
        else:
            tackle_obj = get_object_or_404(RodAndReel, id=tackle_id)   

        if request.user != tackle_obj.user:
            raise Http404('Cannot delete another user''s tackle')    
        tackle_obj.delete()    
        return redirect('tackle', user_id=request.user.id)
