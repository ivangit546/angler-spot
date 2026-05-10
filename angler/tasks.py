from celery import shared_task
from celery.utils.log import get_task_logger
from angler.models.user import User
from angler.models.chat import GroupChat
from django.core.cache import cache


@shared_task
def update_leaderboard():
    top_ten = User.objects.order_by('-points')[:10]
    cache.set('top_ten', top_ten, 60*60*24*7)

    
@shared_task
def account_confirmed(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:       
        return
    if user.is_confirmed == False:
        user.delete()

@shared_task
def hard_delete(gc_id):
    try:
        group_chat = GroupChat.objects.get(id=gc_id)
    except GroupChat.DoesNotExist:
        return
    if group_chat.deleted_at:
        group_chat.delete()    
