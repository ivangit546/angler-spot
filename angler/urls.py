from django.urls import path
from angler.views.registration import Register_View
from angler.views.login import Login_View
from angler.views.main_feed import MainFeed_View
from angler.views.logout import Logout_View
from angler.views.fish_dex import FishDex_View, FishDexEntry

urlpatterns = [
    path('', MainFeed_View.as_view(), name='home_feed'),
    path('register/', Register_View.as_view(), name='register'),
    path('login/', Login_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
    path('fishdex/<int:user_id>', FishDex_View.as_view(), name='fishdex'),
    path('fishdex_entry',FishDexEntry.as_view(), name='fishdex_entry')

]