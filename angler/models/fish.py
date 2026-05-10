from angler.models.user import User
from angler.models.tackle import RodAndReel, Lure
from angler.mixins import ImageRotateMixin
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from cloudinary_storage.storage import MediaCloudinaryStorage
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

def content_file_name(instance, filename):
    """
    Format path for fish_avatar
    """
    fish_group = slugify(instance.fish_group)
    return f'fish/{fish_group}/{filename}'

class Fish(models.Model):
    """
    Represents a Fish that will act as the base (default name, image and height/weight) from Fish Entries to be made from and then added into FishDex
    """
    name = models.CharField(max_length=100, unique=True)
    fish_group = models.CharField(max_length=100, blank=True) 
    weight = models.DecimalField(max_digits=5, decimal_places=1) 
    length = models.DecimalField(max_digits=5, decimal_places=2)
    shiny = models.BooleanField(default=False)  
    fish_avatar = models.ImageField(
    upload_to='fish/',
    storage=MediaCloudinaryStorage()
) 
    
    def __str__(self):
        return self.name
    
    def count(self):
        return Fish.objects.count()
    
   
class FishDex(models.Model):
    """
    Represents a collaction that will house a customizable index of fish objs (entries) a user will be able to add and or remove into
    """     
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unlocked = models.PositiveIntegerField(default=0) 
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

  
class FishEntry(ImageRotateMixin, models.Model):
    """
    A custom fish obj belonging to a sole user with their own data (name, weight, height, image, location...)
    """
    image_field = 'fish_dex_image'      
    
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    fish_dex = models.ForeignKey(FishDex, on_delete=models.CASCADE)
    entry_weight = models.DecimalField(max_digits=5, decimal_places=1)
    entry_length = models.DecimalField(max_digits=5, decimal_places=2)
    fish_dex_image = models.ImageField(upload_to='fishdex_img/', blank=True)
    thumbnail = ImageSpecField(source='fish_dex_image', processors=[ResizeToFill(150, 150, upscale=False)], options={'quality':70})
    tackle = models.ForeignKey(RodAndReel, null=True, blank=True, on_delete=models.SET_NULL)
    lure = models.ForeignKey(Lure, null=True, blank=True, on_delete=models.SET_NULL)
    caught_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        unique_together = ('fish', 'fish_dex')                
           
    def add_points(self):
        """
        If fish entry is shiny add 50 points to user else add 25 points    
        """
        user = self.fish_dex.user
        if self.fish.shiny == True:
            user.points += 50
        else:
            user.points += 25    
        user.save()

    def __str__(self):
        return f"@{self.fish_dex.user.username}'s {self.fish.name} entry in FishDex"

    def get_fish_avatar(self):
        """
        Return FishEntry image
        """
        return self.fish.fish_avatar
    
    def is_shiny(self):
        """
        Return boolean value of is shiny 
        """
        return self.fish.shiny
    

    @property
    def get_fish_color(self):
        """
        Return custom color code based on fish instance's fish_group
        """    
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

