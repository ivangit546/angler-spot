from django.urls import path
from angler.views.registration import Register_View
from angler.views.login import Login_View
from angler.views.main_feed import MainFeed_View
from angler.views.logout import Logout_View
from angler.views.fish_dex import FishDex_View, FishDexEntry
from angler.views.tackle import Tackle_View
from angler.views.friends import Friends_View
urlpatterns = [
    path('', MainFeed_View.as_view(), name='home_feed'),
    path('register/', Register_View.as_view(), name='register'),
    path('login/', Login_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
    path('fishdex/<int:user_id>/', FishDex_View.as_view(), name='fishdex'),
    path('tackle/',Tackle_View.as_view(), name='tackle'),
    path('friend/', Friends_View.as_view(), name='friend'), 


]