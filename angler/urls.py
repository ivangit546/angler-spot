from django.urls import path
from angler.views.registration import RegisterView
from angler.views.login import LoginView
from angler.views.main_feed import MainFeedView
from angler.views.logout import LogoutView
from angler.views.fish_dex import FishDexView, FishDexEntry
from angler.views.tackle import TackleView
from angler.views.friends import FriendsListView
from angler.views.user_profile import UserProfileView
from angler.views.friends import SendFriendRequestView, ManageFriendRequestView, RemoveFriendView
from angler.views.post import CreatePostView, CreateCommentView, LikePostView, DeletePostView, DeleteCommentView
urlpatterns = [
    path('', MainFeedView.as_view(), name='home_feed'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('fishdex/<int:user_id>/', FishDexView.as_view(), name='fishdex'),
    path('tackle/',TackleView.as_view(), name='tackle'),
    path('friendslist/<int:user_id>/', FriendsListView.as_view(), name='friendslist'), 
    path('user_profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('friend_request/<int:user_id>', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('manage_friend_request/<int:user_id>', ManageFriendRequestView.as_view(), name='manage_friend_request'),
    path('remove_friend/<int:user_id>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('post_create', CreatePostView.as_view(), name='post_create'),
    path('post_like/<int:post_id>', LikePostView.as_view(), name='post_like'),
    path('comment_create/<int:post_id>', CreateCommentView.as_view(), name='comment_create')
]