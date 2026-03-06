from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.user import User
from angler.models.tackle import RodAndReel, Lure
from angler.forms.tackle import RodAndReelForm, LureForm
from django.contrib.auth.mixins import LoginRequiredMixin

class TackleView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        rod_and_reels = RodAndReel.objects.filter(user=user)
        lures = Lure.objects.filter(user=user)
        context ={'user':user,
                   'rod_and_reels':rod_and_reels,
                     'lures':lures}
        return render(request, 'angler/tackle.html', context)
        
class RodAndReelCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get (self, request):
        form = RodAndReelForm()
        return render(request, 'angler/rod_and_reel/create.html', {'form':form})
    
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
        return render(request, 'angler/lure/create.html', {'form':form})

    def post(self, request):
        user = request.user
        lure_form = LureForm(data=request.POST)
        if lure_form.is_valid():
            lure = lure_form.save(commit=False)
            lure.user = user
            lure.save()
        return redirect('tackle', user.id)

