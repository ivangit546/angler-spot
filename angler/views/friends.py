from angler.models.user import User
from angler.models.friends import FriendList, FriendRequest
from django.views import View
from django.shortcuts import render

class Friends_View(View):
    def get(self, request):
        user=request.user
        friends = FriendList.objects.get(user=user).friends.all()
        is_friend=FriendList.objects.get(user=user).is_friend(User.objects.get(id=3))
        context = {
            'friends':friends,
        }
        return render(request, 'angler/friend.html', context)
    
    #change view to depend on user_id