from angler.models.user import User, Profile
from django.forms import modelform_factory
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import  redirect, render
from django.views import View


class SettingsView(LoginRequiredMixin, View):
    login_url = '/login/'
    private_form = modelform_factory(User, fields=('is_private',))
    def get(self, request):
        form = self.private_form(instance=request.user)
        return render(request, 'angler/user/settings.html', {'form':form})
    
    def post(self, request):
        form = self.private_form(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()     
        return redirect(request.path)    

class DeleteAccountView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request):
        user = request.user
        user.delete()
        return redirect('/')
    
class EditAccountView(LoginRequiredMixin, View):
    login_url = '/login/'
    username_form = modelform_factory(User, fields=('username',))
    email_form = modelform_factory(User, fields=('email',))
    def get(self, request, action):
        if action == 'Username':
             form = self.username_form(instance=request.user)
        elif action == 'Email':
            form = self.email_form(instance=request.user)
        elif action == 'Password':
            form = PasswordChangeForm(user=request.user)  
        else:
            raise ValueError('Invalid Edit Action') 
        context = {'form': form, 'action':action}
           
        return render(request, 'angler/user/edit_user.html', context)
    
    def post(self, request, action):
        if action == 'Password':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password Change Successfully')
                return redirect('settings')

            messages.error(request, f'{form.errors}')
        elif action == 'Username':
            form = self.username_form(data=request.POST, instance=request.user) 
        else:
            form = self.email_form(data=request.POST, instance=request.user)
        

        if form.is_valid():
            form.save()
            messages.success(request, f'Successful {action} Change')

        return redirect('settings')    
        