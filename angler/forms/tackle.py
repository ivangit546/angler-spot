from django import forms 
from angler.models.tackle import RodAndReel, Lure

class ReelAndRod(forms.ModelForm):
    class Meta:
        model = RodAndReel
        fields = ('name', 'rod_length','rod_length', 'line', 'line_length', 'leader', 'leader_length')


class Lure(forms.ModelForm):
    class Meta:
        model = Lure
        fields = ('name','live_bait', 'lure_type', 'trailer', 'description')