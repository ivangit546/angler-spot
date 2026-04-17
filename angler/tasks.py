from celery import shared_task
from angler.models.user import User
from django.core.cache import cache

@shared_task
def update_leaderboard():
    top_ten = User.objects.order_by('-points')[:10]
    cache.set('top_ten', top_ten, 60*60*24*7)