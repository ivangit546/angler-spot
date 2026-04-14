from django import forms
from angler.models.user import User
from angler.models.user import Profile



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email','password','confirm_password',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords must match"
            )
            


class ProfileForm(forms.ModelForm):    
    class Meta:
        model = Profile
        fields = ['profile_image', 'profile_name',]
