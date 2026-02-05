from django.db import models
from angler.models.user import User

class RodAndReel(models.Model):
    LINE_CHOICES = (('monofilament', 'Mono'),
                     ('fluorocarbon', 'Flouro'),
                       ('braid', 'Braid'))
    REEL_CHOICES = (('spinning','Spinning'),
                     ('baitcaster','Baitcaster'),
                       ('spincast','Spincast'), ('fly', 'Fly'),
                         ('conventional', 'Conventional'))
    ROD_ACTION_CHOICES = (('slow','Slow'), 
                          ('medium', 'Medium'), 
                          ('fast', 'Fast'), 
                          ('extra fast', 'Extra Fast'))
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rod_length = models.DecimalField(default=6, max_digits=3, decimal_places=1)
    line = models.CharField(max_length=100, choices=LINE_CHOICES)
    line_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    leader = models.CharField(max_length=100, choices=LINE_CHOICES, null=True, blank=True)
    leader_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Lure(models.Model):
    LURE_CHOICES = (('bait', 'Bait'),
                     ('lure', 'Lure'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    lure_type = models.CharField(max_length=100, choices=LURE_CHOICES)
    live_bait = models.BooleanField(default=False)
    trailer = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
