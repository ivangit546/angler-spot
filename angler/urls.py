from django.urls import path
from angler.views.registration import RegisterView
from angler.views.login import LoginView
from angler.views.main_feed import MainFeedView
from angler.views.logout import LogoutView
from angler.views.fish_dex import FishDexView, FishDexEntryView, FishDexDetailView
from angler.views.tackle import RodAndReelCreateView, TackleView, LureCreateView
from angler.views.friends import FriendsListView
from angler.views.user_profile import UserProfileView
from angler.views.friends import SendFriendRequestView, ManageFriendRequestView, RemoveFriendView
from angler.views.post import CreatePostView, CreateCommentView, LikePostView, DeletePostView, DeleteCommentView, LikeCommentView, PostDetailView, CreateReplyView
urlpatterns = [
   
    #Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    #Home page
    path('', MainFeedView.as_view(), name='home_feed'),


    #Post & Comments
    path('post_create', CreatePostView.as_view(), name='post_create'),
    path('post_delete/<int:post_id>', DeletePostView.as_view(), name='post_delete'),
    path('post_detail/<int:post_id>', PostDetailView.as_view(), name='post_detail'),
    path('post_like/<int:post_id>', LikePostView.as_view(), name='post_like'),
    path('comment_create/<int:post_id>', CreateCommentView.as_view(), name='comment_create'),
    path('comment_delete/<int:comment_id>', DeleteCommentView.as_view(), name='comment_delete'),
    path('comment_like/<int:comment_id>', LikeCommentView.as_view(), name='comment_like'),
    path('reply_create/<int:comment_id>', CreateReplyView.as_view(), name='reply_create'),
 
    #Friends & Friend Request
    path('friendslist/<int:user_id>/', FriendsListView.as_view(), name='friendslist'), 
    path('friend_request/<int:user_id>', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('manage_friend_request/<int:user_id>', ManageFriendRequestView.as_view(), name='manage_friend_request'),
    path('remove_friend/<int:user_id>/', RemoveFriendView.as_view(), name='remove_friend'),
    
    #FishDex
    path('fishdex/<int:user_id>/', FishDexView.as_view(), name='fishdex'),
    path('fishdex_entry/', FishDexEntryView.as_view(), name='fishdex_entry'),
    path('fishdex_detail/<int:fishdex_id>/<int:fish_entry_id>/', FishDexDetailView.as_view(), name='fishdex_detail'),
    
    #Tackle
    path('rod&reel_create/',RodAndReelCreateView.as_view(), name='rod_reel_create'),
    path('lure_create/',LureCreateView.as_view(), name='lure_create'),
    path('user_profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('tackle/<int:user_id>', TackleView.as_view(), name='tackle'),
      
]