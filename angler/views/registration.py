from django.shortcuts import redirect, render
from django.views import View
from angler.models import Post, User, Profile
from angler.forms.user import UserRegistrationForm, ProfileForm
from django.contrib.auth import login




class Register_View(View):
    
    def get(self, request):
        user_form = UserRegistrationForm
        profile_form = ProfileForm
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
            # login(request, user) TODO uncomment after login form/view and template are done
            return redirect('login')
        else:
            print(user_form.errors, profile_form.errors)
        return render(request, 'angler/register.html', {'user_form':user_form, 'profile_form':profile_form})        