from django.contrib import admin
from angler.models.user import User
from angler.models.user import Profile
from angler.models.post import Post
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.tackle import RodAndReel, Lure

admin.site.register(User),
admin.site.register(Post),
admin.site.register(Profile),
admin.site.register(Fish),
admin.site.register(FishEntry),
admin.site.register(RodAndReel),
admin.site.register(Lure),


class FishEntryInline(admin.TabularInline):  
    model = FishEntry

@admin.register(FishDex)
class FishDexAdmin(admin.ModelAdmin):
    inlines = [FishEntryInline] 


