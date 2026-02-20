from django.contrib import admin
from angler.models.user import User
from angler.models.user import Profile
from angler.models.post import Post
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.tackle import RodAndReel, Lure
from angler.models.friends import FriendList, FriendRequest

admin.site.register(User),
admin.site.register(Post),
admin.site.register(Profile),
admin.site.register(Fish),
admin.site.register(FishEntry),
admin.site.register(RodAndReel),
admin.site.register(Lure),
admin.site.register(FriendList),
admin.site.register(FriendRequest),

class FishEntryInline(admin.TabularInline):  
    model = FishEntry

@admin.register(FishDex)
class FishDexAdmin(admin.ModelAdmin):
    inlines = [FishEntryInline] 


