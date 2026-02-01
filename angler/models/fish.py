from django.db import models
from user import User
from django.conf import settings
from django.forms import ImageField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Fish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fish_group = models.CharField(max_length=100, blank=True) #i.e bass is the group and the fish name would be large mouth bass
    weight = models.DecimalField(max_digits=5, decimal_places=1) # i.e 1230.9 
    length = models.DecimalField(max_digits=5, decimal_places=2) # standard unnit will be inches (form will accept feet and or inches then convert to inches) i.e 234.43
    shiny = models.BooleanField(blank=True, default=False)
    shiny_type = models.CharField(max_length=100, null=True) # might remove later as it could be redundant-> change 'shiny' to charfield and if not null then alr has boolean value assumed(true)
    # fish_image = 
    # user_image = 

class FishDex(models.Model):
    name = models.CharField(max_length=120)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unlocked = models.PositiveIntegerField(default=0) # number of unlocked fish (i.e a tally to display) also can be removed as might be redundant as we can query # of fishes to total number of fish availible
    fishes = models.ManyToManyField(Fish, blank=True)


# will have to create a Post like model for fishdex entries that will allow users to TODO use through for many to many to allow personal fish entery data like weight without changing global value 