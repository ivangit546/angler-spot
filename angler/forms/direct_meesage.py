from django.forms import ModelForm
from django import forms
from angler.models.chat import DirectMessage, GroupChat

class DirectMessageCreateForm(ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['text', 'image']
