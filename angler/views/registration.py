from django.shortcuts import redirect, render
from django.views import View
from angler.forms.user import UserRegistrationForm, ProfileForm
from django.contrib.auth import login
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.friends import FriendList

class RegisterView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect ('/')
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'angler/register.html', {'user_form':user_form, 'profile_form':profile_form})
    
    def post(self, request):
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password']) # TODO works but not displaying error, possible place or in registration template 
            user = user_form.save()
            profile = profile_form.save(commit=False) #stop django from saving this instance of profile into the database without a user object in its one to one relationship yet
            profile.user = user
            profile.save()
            fish_dex = FishDex.objects.create(user=user) #TODO replace and do logic in fish model file upon user creation via signal
            fish_dex.save()
            friends_list = FriendList.objects.create(user=user)
            friends_list.save()
            login(request, user)
            return redirect('/')
        else:
            print(user_form.errors, profile_form.errors)
        return render(request, 'angler/register.html', {'user_form':user_form, 'profile_form':profile_form})        