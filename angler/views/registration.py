from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from angler.forms.user import UserRegistrationForm, ProfileForm
from django.contrib.auth import login
from angler.models.fish import FishDex
from angler.models.friends import FriendList
from angler.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from angler.tokens import account_activation_token
from django.core.mail import EmailMessage
from angler.tasks import account_confirmed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class RegisterView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect ('/')
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'angler/registration/register.html', {'user_form':user_form, 'profile_form':profile_form})
    
    def post(self, request):
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user = user_form.save()
            profile = profile_form.save(commit=False) 
            profile.user = user
            profile.save()
            fish_dex = FishDex.objects.create(user=user) 
            fish_dex.save()
            friends_list = FriendList.objects.create(user=user)
            friends_list.save()
            mail_subject = 'Activate account'
            message = render_to_string('angler/emails/account_confirmation.html', {'user':user,
                                                                                'domain':get_current_site(request),
                                                                                'uid':urlsafe_base64_encode(force_bytes(user.id)), 
                                                                                'token':account_activation_token.make_token(user)})
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            account_confirmed.apply_async(args=[user.id], countdown=24*60*60)
            messages.success(request, 'Account confirmation email sent')
            login(request, user)
            return redirect('/')
        return render(request, 'angler/registration/register.html', {'user_form':user_form, 'profile_form':profile_form}) 
           
class AccountActiavtionView(View):   
    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=uid)
        if user is not None and account_activation_token.check_token(user,token):
            user.is_confirmed = True
            user.save()
            messages.success(request, 'Account has been confirmed')
        else:
            messages.error(request,'Account confirmation link is invalid')
        return redirect('/')       
    
class PasswordResetView():
    pass    
