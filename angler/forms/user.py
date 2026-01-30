from django import forms
from angler.models import User, Profile



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email','password','confirm_password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password is None:
            self.add_error('password', "Enter a password")
            return cleaned_data
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")
            


class ProfileForm(forms.ModelForm):    
    class Meta:
        model = Profile
        fields = ['profile_image', 'profile_name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_name'].widget.attrs.update({
            'class': 'form-control'
        })