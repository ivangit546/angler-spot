from django.contrib import admin
from angler.models.user import User
from angler.models.user import Profile
from angler.models.post import Post, Comment, Like
from angler.models.fish import Fish, FishDex, FishEntry
from angler.models.tackle import RodAndReel, Lure
from angler.models.friends import FriendList, FriendRequest
from angler.models.notification import Notification
from angler.models.chat import GroupChat, DirectMessage, Reaction

admin.site.register(User),
admin.site.register(Post),
admin.site.register(Profile),
admin.site.register(Fish),
admin.site.register(FishEntry),
admin.site.register(RodAndReel),
admin.site.register(Lure),
admin.site.register(FriendList),
admin.site.register(FriendRequest),
admin.site.register(Comment),
admin.site.register(Like),
admin.site.register(Notification),
admin.site.register(GroupChat),
admin.site.register(DirectMessage),
admin.site.register(Reaction),


class FishEntryInline(admin.TabularInline):  
    model = FishEntry

@admin.register(FishDex)
class FishDexAdmin(admin.ModelAdmin):
    inlines = [FishEntryInline] 


