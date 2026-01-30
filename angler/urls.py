from django.urls import path
from angler.views.registration import Register_View
from angler.views.login import Login_View
from angler.views.main_feed import MainFeed_View

urlpatterns = [
    path('', MainFeed_View.as_view(), name='home_feed'),
    path('register/', Register_View.as_view(), name='register'),
    path('login/', Login_View.as_view(), name='login'),
    
]