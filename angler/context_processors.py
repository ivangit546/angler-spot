from angler.models.notification import Notification
from angler.models.chat import GroupChat
from django.contrib.contenttypes.models import ContentType


def notification_counter(request):
    if request.user.is_authenticated:
        gc_ct = ContentType.objects.get_for_model(GroupChat)
        notification_count = Notification.objects.filter(recipient=request.user, is_read=False).exclude(content_type=gc_ct).count()
        if notification_count > 99:
            notification_count = '99+'
        return{
            'notification_count':notification_count
            }
    return {}

    
def message_counter(request):
    if request.user.is_authenticated:
        gc_ct = ContentType.objects.get_for_model(GroupChat)
        message_notification_count = Notification.objects.filter(content_type=gc_ct, recipient=request.user, is_read=False).count()
        if message_notification_count > 99:
            message_notification_count = '99+'
        return{
            'message_notification_count':message_notification_count
            }
    return {}
