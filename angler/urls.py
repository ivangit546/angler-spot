from django.urls import path
from .views import MainFeed_View, Register_View, Login_View

urlpatterns = [
    path('', MainFeed_View.as_view(), name='home_feed'),
    path('register/', Register_View.as_view(), name='register'),
    path('login/', Login_View.as_view(), name='login'),
    
]