from django import forms
from angler.models import User, Profile



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','password','email')

class ProfileForm(forms.ModelForm):    
    profile_image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['profile_image']
