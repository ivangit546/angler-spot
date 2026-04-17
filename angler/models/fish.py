from django.db import models
from angler.models.user import User
from angler.models.user import User
from django.utils.text import slugify
from angler.models.tackle import RodAndReel, Lure
from django_resized import ResizedImageField
def content_file_name(instance, filename):
    fish_group = slugify(instance.fish_group)
    return f'fish/{fish_group}/{filename}'

class Fish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fish_group = models.CharField(max_length=100, blank=True) #i.e bass is the group and the fish name would be large mouth bass
    weight = models.DecimalField(max_digits=5, decimal_places=1) # i.e 1230.9 
    length = models.DecimalField(max_digits=5, decimal_places=2) # standard unnit will be inches (form will accept feet and or inches then convert to inches) i.e 234.43
    shiny = models.BooleanField(default=False) 
    fish_avatar = models.ImageField(upload_to=content_file_name) #will be stock image for type of fish
    

    def __str__(self):
        return self.name
    
    def count(self):
        return Fish.objects.count()
    
class FishDex(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unlocked = models.PositiveIntegerField(default=0) # number of unlocked fish (i.e a tally to display) also can be removed as might be redundant as we can query # of fishes to total number of fish availible
    fishes = models.ManyToManyField(Fish, blank=True, through='FishEntry', related_name='fish_dexes')
    
    def __str__(self):
        return self.user.username + "'s fishDex" 
     
    def unlock(self):
        self.unlocked += 1
        self.save()

    def lock(self):
        if self.unlocked - 1 >= 0:
            self.unlocked -= 1
            self.save()     
    
class FishEntry(models.Model):
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    fish_dex = models.ForeignKey(FishDex, on_delete=models.CASCADE)
    entry_weight = models.DecimalField(max_digits=5, decimal_places=1)
    entry_length = models.DecimalField(max_digits=5, decimal_places=2)
    fish_dex_image = ResizedImageField(size=[1600, 900], upload_to='fishdex_img/', blank=True)
    thumbnail = ResizedImageField(size=[150,150], crop=['middle', 'center'], upload_to='thumbnails/', blank=True)
    tackle = models.ForeignKey(RodAndReel, null=True, blank=True, on_delete=models.SET_NULL)
    lure = models.ForeignKey(Lure, null=True, blank=True, on_delete=models.SET_NULL)
    caught_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    class Meta:
        unique_together = ('fish', 'fish_dex')  

    def add_points(self):
        user = self.fish_dex.user
        if self.fish.shiny == True:
            user.points += 50
        else:
            user.points += 25    
        user.save()
    def __str__(self):
        return f"@{self.fish_dex.user.username}'s {self.fish.name} entry in FishDex"
    def get_fish_avatar(self):
        return self.fish.fish_avatar
    def is_shiny(self):
        return self.fish.shiny
    @property
    def get_fish_color(self):
        match self.fish.fish_group:
            case 'Bass':
                return '#0EAD3F'
            case 'Carp':
                return '#5aed9f'
            case 'Catfish':
                return '#0ead83'
            case 'Drum':
                return '#ded309'
            case 'Gar':
                return '#89f266'
            case 'Panfish':
                return '#f5a631'
            case 'Pike':
                return '#31b4f5'
            case 'Salmon':
                return '#5314f5'
            case 'Sturgeon':
                return '#f01a81'
            case 'Trout':
                return '#9f55ed'
            case 'Walleye':
                return '#bf0b38'
            case _:
                raise ValueError(f'{self.fish.fish_group} : is invalid')     

