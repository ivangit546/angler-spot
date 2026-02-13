from django import forms
from angler.models.fish import FishEntry, FishDex, Fish


class FishDexEntryForm(forms.ModelForm):
    
    class Meta:
        model = FishEntry
        fields = ('fish','entry_weight', 'entry_length', 'fish_dex_image')

