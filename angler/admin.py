from django.contrib import admin
from .models.user import User
from .models.user import Profile
from .models.post import Post
from .models.fish import Fish, FishDex


admin.site.register(User),
admin.site.register(Post),
admin.site.register(Profile),


