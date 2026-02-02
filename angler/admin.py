from django.contrib import admin
from angler.models.user import User
from angler.models.user import Profile
from angler.models.post import Post
from angler.models.fish import Fish, FishDex, FishEntry


admin.site.register(User),
admin.site.register(Post),
admin.site.register(Profile),
admin.site.register(Fish),
admin.site.register(FishEntry),


class FishEntryInline(admin.TabularInline): # 
    model = FishEntry

@admin.register(FishDex)
class FishDexAdmin(admin.ModelAdmin):
    inlines = [FishEntryInline] 


