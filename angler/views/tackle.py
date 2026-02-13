from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import get_object_or_404
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.user import User
from angler.forms.tackle import ReelAndRod, Lure


class Tackle_View(View):

    def get (self, request):
        rod_real_form = ReelAndRod()
        lure_form = Lure()
        return render(request, 'angler/tackle.html', {'rod_real_form':rod_real_form, 'lure_form':lure_form})
