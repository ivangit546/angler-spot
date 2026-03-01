from django import forms 
from angler.models.tackle import RodAndReel, Lure

class RodAndReelForm(forms.ModelForm):
    class Meta:
        model = RodAndReel
        fields = ('name', 'rod_length','rod_length', 'line', 'line_length', 'leader', 'leader_length')


class LureForm(forms.ModelForm):
    class Meta:
        model = Lure
        fields = ('name', 'live_bait', 'lure_type', 'trailer', 'description')